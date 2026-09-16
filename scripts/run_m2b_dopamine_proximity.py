#!/usr/bin/env python3
"""Run M2B: dopamine-connectivity proximity for curated candidate cell types.

This analysis deliberately bridges only cell types with an explicit MaleCNS
annotation rule. It never assigns Fly Cell Atlas gene expression to individual
MaleCNS body IDs. Candidate-linked neuron groups are tested against neurons
matched by anatomical family, connection-strength quantile, and degree
quantile using a stratified bootstrap null.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.feather as feather
import pyarrow.ipc as ipc


ROOT = Path(__file__).resolve().parents[1]
ANNOTATIONS = ROOT / "data/flat-connectome/body-annotations-male-cns-v1.0-minconf-0.5.feather"
NEUROTRANSMITTERS = ROOT / "data/flat-connectome/body-neurotransmitters-male-cns-v1.0.feather"
WEIGHTS = ROOT / "data/flat-connectome/connectome-weights-male-cns-v1.0-minconf-0.5.feather"
DOPAMINE_TARGETS = ROOT / "outputs/malecns-dopamine-target-neurons.csv"
OUTPUT = ROOT / "outputs"

PERMUTATIONS = 10_000
SEED = 20260916
MATCH_QUANTILES = 5

ANNOTATION_FIELDS = [
    "bodyId", "type", "class", "subclass", "superclass", "supertype",
    "flywireType", "hemibrainType", "mancType", "synonyms",
]


def clean(value) -> str:
    return "" if value is None else str(value)


def bh_adjust(indices: list[int], p_values: list[float]) -> dict[int, float]:
    ordered = sorted(indices, key=lambda index: p_values[index])
    adjusted = {}
    running = 1.0
    n = len(ordered)
    for position in range(n - 1, -1, -1):
        index = ordered[position]
        rank = position + 1
        running = min(running, p_values[index] * n / rank)
        adjusted[index] = running
    return adjusted


def match_family(superclass: str) -> str:
    value = superclass or ""
    if value.startswith("ol_") or value.startswith("visual_"):
        return "optic_visual"
    if value.startswith("cb_"):
        return "central_brain"
    if value.startswith("vnc_"):
        return "ventral_nerve_cord"
    if "ascending" in value or "descending" in value:
        return "long_range"
    if value == "ENS":
        return "enteric"
    return "other"


def load_dopamine_ids() -> np.ndarray:
    ids = []
    with DOPAMINE_TARGETS.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["dopamine_evidence"] == "consensus_dopamine":
                ids.append(int(row["bodyId"]))
    if not ids:
        raise RuntimeError("No consensus dopamine neurons found")
    return np.array(sorted(set(ids)), dtype=np.int64)


def build_groups(rows: list[dict], annotated_ids: np.ndarray) -> tuple[list[dict], dict[str, np.ndarray]]:
    consensus_octopamine = feather.read_table(NEUROTRANSMITTERS, columns=["body", "consensus_nt"])
    oct_mask = pc.equal(consensus_octopamine["consensus_nt"], "octopamine")
    oct_ids = set(pc.filter(consensus_octopamine["body"], oct_mask).to_pylist())

    definitions = [
        {
            "bridge_id": "lar-lawf2",
            "linked_human_genes": "PTPRF",
            "linked_fly_genes": "Lar",
            "fca_cell_type": "lamina wide-field 2 neuron",
            "rule": "type == Lawf2 or flywireType == Lawf2",
            "kind": "candidate",
            "select": lambda row: row["type"] == "Lawf2" or row["flywireType"] == "Lawf2",
        },
        {
            "bridge_id": "lar-tmy4",
            "linked_human_genes": "PTPRF",
            "linked_fly_genes": "Lar",
            "fca_cell_type": "transmedullary Y neuron TmY4",
            "rule": "type == TmY4 or flywireType == TmY4",
            "kind": "candidate",
            "select": lambda row: row["type"] == "TmY4" or row["flywireType"] == "TmY4",
        },
        {
            "bridge_id": "lar-octopamine",
            "linked_human_genes": "PTPRF",
            "linked_fly_genes": "Lar",
            "fca_cell_type": "adult octopaminergic neuron",
            "rule": "consensus_nt == octopamine",
            "kind": "candidate",
            "select": lambda row: row["bodyId"] in oct_ids,
        },
        {
            "bridge_id": "foxp-cg32486-dm4",
            "linked_human_genes": "FOXP1 | FOXP2 | CYHR1",
            "linked_fly_genes": "FoxP | CG32486",
            "fca_cell_type": "distal medullary amacrine neuron Dm4",
            "rule": "type == Dm4 or flywireType == Dm4; excludes DM4 olfactory glomerular types",
            "kind": "candidate",
            "select": lambda row: row["type"] == "Dm4" or row["flywireType"] == "Dm4",
        },
        {
            "bridge_id": "foxp-lc10c",
            "linked_human_genes": "FOXP1 | FOXP2",
            "linked_fly_genes": "FoxP",
            "fca_cell_type": "lobula columnar neuron LC10c",
            "rule": "flywireType == LC10c",
            "kind": "candidate",
            "select": lambda row: row["flywireType"] == "LC10c",
        },
        {
            "bridge_id": "camki-photoreceptor",
            "linked_human_genes": "CAMKV",
            "linked_fly_genes": "CaMKI",
            "fca_cell_type": "photoreceptor neuron family",
            "rule": "superclass == ol_sensory",
            "kind": "candidate",
            "select": lambda row: row["superclass"] == "ol_sensory",
        },
        {
            "bridge_id": "sema1a-hugin",
            "linked_human_genes": "SEMA6D",
            "linked_fly_genes": "Sema1a",
            "fca_cell_type": "Hugin neuron",
            "rule": "type == Hugin-RG or flywireType == Hugin-RG",
            "kind": "candidate",
            "select": lambda row: row["type"] == "Hugin-RG" or row["flywireType"] == "Hugin-RG",
        },
        {
            "bridge_id": "sema1a-itp",
            "linked_human_genes": "SEMA6D",
            "linked_fly_genes": "Sema1a",
            "fca_cell_type": "ITP neuron",
            "rule": "type == ITP or flywireType == ITP",
            "kind": "candidate",
            "select": lambda row: row["type"] == "ITP" or row["flywireType"] == "ITP",
        },
        {
            "bridge_id": "sema1a-alpn",
            "linked_human_genes": "SEMA6D",
            "linked_fly_genes": "Sema1a",
            "fca_cell_type": "antennal lobe projection neuron",
            "rule": "class == ALPN",
            "kind": "candidate",
            "select": lambda row: row["class"] == "ALPN",
        },
        {
            "bridge_id": "cg32486-crz",
            "linked_human_genes": "CYHR1",
            "linked_fly_genes": "CG32486",
            "fca_cell_type": "adult corazonin neuron",
            "rule": "flywireType == CRZ",
            "kind": "candidate",
            "select": lambda row: row["flywireType"] == "CRZ",
        },
        {
            "bridge_id": "cg32486-dm1",
            "linked_human_genes": "CYHR1",
            "linked_fly_genes": "CG32486",
            "fca_cell_type": "distal medullary amacrine neuron Dm1",
            "rule": "type == Dm1 or flywireType == Dm1",
            "kind": "candidate",
            "select": lambda row: row["type"] == "Dm1" or row["flywireType"] == "Dm1",
        },
        {
            "bridge_id": "calibration-kenyon-cell",
            "linked_human_genes": "",
            "linked_fly_genes": "",
            "fca_cell_type": "Kenyon cell positive comparator",
            "rule": "class == Kenyon_Cell",
            "kind": "calibration",
            "select": lambda row: row["class"] == "Kenyon_Cell",
        },
        {
            "bridge_id": "calibration-mbon",
            "linked_human_genes": "",
            "linked_fly_genes": "",
            "fca_cell_type": "mushroom body output neuron positive comparator",
            "rule": "class == MBON",
            "kind": "calibration",
            "select": lambda row: row["class"] == "MBON",
        },
    ]

    groups = {}
    bridge_rows = []
    for definition in definitions:
        selected = np.array(
            [row["bodyId"] for row in rows if definition["select"](row)],
            dtype=np.int64,
        )
        selected = np.intersect1d(selected, annotated_ids, assume_unique=False)
        groups[definition["bridge_id"]] = selected
        bridge_rows.append({
            key: value for key, value in definition.items() if key != "select"
        } | {"annotated_neurons": len(selected)})
    return bridge_rows, groups


def add_by_index(target: np.ndarray, indices: np.ndarray, values: np.ndarray | None = None) -> None:
    if not len(indices):
        return
    if values is None:
        target += np.bincount(indices, minlength=len(target)).astype(target.dtype, copy=False)
    else:
        target += np.bincount(indices, weights=values, minlength=len(target)).astype(target.dtype, copy=False)


def scan_connectome(ids: np.ndarray, dopamine_ids: np.ndarray) -> dict[str, np.ndarray | int]:
    n = len(ids)
    total_in_weight = np.zeros(n, dtype=np.int64)
    total_out_weight = np.zeros(n, dtype=np.int64)
    in_degree = np.zeros(n, dtype=np.int64)
    out_degree = np.zeros(n, dtype=np.int64)
    dopamine_in_weight = np.zeros(n, dtype=np.int64)
    dopamine_out_weight = np.zeros(n, dtype=np.int64)
    dopamine_in_edges = np.zeros(n, dtype=np.int64)
    dopamine_out_edges = np.zeros(n, dtype=np.int64)
    scanned = 0

    with pa.memory_map(str(WEIGHTS), "r") as source:
        reader = ipc.open_file(source)
        for batch_index in range(reader.num_record_batches):
            batch = reader.get_batch(batch_index)
            pre = batch["body_pre"].to_numpy(zero_copy_only=False)
            post = batch["body_post"].to_numpy(zero_copy_only=False)
            weight = batch["weight"].to_numpy(zero_copy_only=False)
            scanned += batch.num_rows

            pre_index = np.searchsorted(ids, pre)
            post_index = np.searchsorted(ids, post)
            valid_pre = pre_index < n
            valid_post = post_index < n
            valid_pre[valid_pre] &= ids[pre_index[valid_pre]] == pre[valid_pre]
            valid_post[valid_post] &= ids[post_index[valid_post]] == post[valid_post]

            add_by_index(total_out_weight, pre_index[valid_pre], weight[valid_pre])
            add_by_index(out_degree, pre_index[valid_pre])
            add_by_index(total_in_weight, post_index[valid_post], weight[valid_post])
            add_by_index(in_degree, post_index[valid_post])

            dopamine_pre = np.isin(pre, dopamine_ids, assume_unique=False)
            dopamine_post = np.isin(post, dopamine_ids, assume_unique=False)
            selected_in = valid_post & dopamine_pre
            selected_out = valid_pre & dopamine_post
            add_by_index(dopamine_in_weight, post_index[selected_in], weight[selected_in])
            add_by_index(dopamine_in_edges, post_index[selected_in])
            add_by_index(dopamine_out_weight, pre_index[selected_out], weight[selected_out])
            add_by_index(dopamine_out_edges, pre_index[selected_out])

            if (batch_index + 1) % 250 == 0 or batch_index + 1 == reader.num_record_batches:
                print(
                    f"connectome batches={batch_index + 1}/{reader.num_record_batches}, "
                    f"rows={scanned:,}",
                    flush=True,
                )

    return {
        "total_in_weight": total_in_weight,
        "total_out_weight": total_out_weight,
        "in_degree": in_degree,
        "out_degree": out_degree,
        "dopamine_in_weight": dopamine_in_weight,
        "dopamine_out_weight": dopamine_out_weight,
        "dopamine_in_edges": dopamine_in_edges,
        "dopamine_out_edges": dopamine_out_edges,
        "rows_scanned": scanned,
    }


def quantile_bins(values: np.ndarray, families: np.ndarray, eligible: np.ndarray) -> np.ndarray:
    result = np.full(len(values), -1, dtype=np.int16)
    for family in sorted(set(families[eligible])):
        mask = eligible & (families == family)
        family_values = np.log1p(values[mask].astype(np.float64))
        if not len(family_values):
            continue
        edges = np.quantile(family_values, np.arange(1, MATCH_QUANTILES) / MATCH_QUANTILES)
        result[mask] = np.searchsorted(edges, family_values, side="right")
    return result


def stratified_null(
    values: np.ndarray,
    selected: np.ndarray,
    background: np.ndarray,
    strata: np.ndarray,
    rng: np.random.Generator,
) -> tuple[float, float, float, int]:
    selected_indices = np.flatnonzero(selected)
    observed = float(values[selected_indices].mean())
    counts = Counter(strata[selected_indices].tolist())
    null_sum = np.zeros(PERMUTATIONS, dtype=np.float64)
    used = 0
    for stratum, count in counts.items():
        pool = values[background & (strata == stratum)]
        if not len(pool):
            raise RuntimeError(f"No matched background neurons for stratum {stratum}")
        used += count
        chunk_size = max(1, min(PERMUTATIONS, 2_000_000 // max(count, 1)))
        for start in range(0, PERMUTATIONS, chunk_size):
            stop = min(PERMUTATIONS, start + chunk_size)
            choices = rng.integers(0, len(pool), size=(stop - start, count))
            null_sum[start:stop] += pool[choices].sum(axis=1)
    null_values = null_sum / used
    null_mean = float(null_values.mean())
    p_value = float((np.count_nonzero(null_values >= observed) + 1) / (PERMUTATIONS + 1))
    return observed, null_mean, p_value, used


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    annotation_table = feather.read_table(ANNOTATIONS, columns=ANNOTATION_FIELDS)
    raw_rows = annotation_table.to_pylist()
    rows = [{field: clean(row.get(field)) for field in ANNOTATION_FIELDS} for row in raw_rows]
    for raw, row in zip(raw_rows, rows):
        row["bodyId"] = int(raw["bodyId"])

    order = np.argsort(np.array([row["bodyId"] for row in rows], dtype=np.int64))
    rows = [rows[index] for index in order]
    ids = np.array([row["bodyId"] for row in rows], dtype=np.int64)
    if len(np.unique(ids)) != len(ids):
        raise RuntimeError("Duplicate bodyId values in annotation table")
    families = np.array([match_family(row["superclass"]) for row in rows], dtype=object)

    dopamine_ids = load_dopamine_ids()
    bridge_rows, groups = build_groups(rows, ids)
    metrics = scan_connectome(ids, dopamine_ids)

    total_in = metrics["total_in_weight"]
    total_out = metrics["total_out_weight"]
    in_degree = metrics["in_degree"]
    out_degree = metrics["out_degree"]
    dopamine_in = metrics["dopamine_in_weight"]
    dopamine_out = metrics["dopamine_out_weight"]

    in_fraction = np.divide(
        dopamine_in, total_in, out=np.zeros(len(ids), dtype=np.float64), where=total_in > 0
    )
    out_fraction = np.divide(
        dopamine_out, total_out, out=np.zeros(len(ids), dtype=np.float64), where=total_out > 0
    )
    eligible_in = total_in > 0
    eligible_out = total_out > 0
    in_strength_bin = quantile_bins(total_in, families, eligible_in)
    in_degree_bin = quantile_bins(in_degree, families, eligible_in)
    out_strength_bin = quantile_bins(total_out, families, eligible_out)
    out_degree_bin = quantile_bins(out_degree, families, eligible_out)

    family_codes = {name: index for index, name in enumerate(sorted(set(families)))}
    family_code = np.array([family_codes[name] for name in families], dtype=np.int32)
    in_strata = family_code * 100 + in_strength_bin * 10 + in_degree_bin
    out_strata = family_code * 100 + out_strength_bin * 10 + out_degree_bin

    dopamine_mask = np.isin(ids, dopamine_ids)
    rng = np.random.default_rng(SEED)
    results = []

    for bridge in bridge_rows:
        group_ids = groups[bridge["bridge_id"]]
        group_mask = np.isin(ids, group_ids)
        # Each hypothesis is compared with all other annotated neurons in the
        # same matched strata. Excluding other candidate-linked groups would
        # distort the background, especially in the optic system where the
        # photoreceptor group is large.
        excluded = group_mask | dopamine_mask

        for direction, values, eligible, strata, total_weight, dopamine_weight, degree in [
            ("dopamine_to_group", in_fraction, eligible_in, in_strata, total_in, dopamine_in, in_degree),
            ("group_to_dopamine", out_fraction, eligible_out, out_strata, total_out, dopamine_out, out_degree),
        ]:
            selected = group_mask & eligible
            background = (~excluded) & eligible
            if not np.any(selected):
                observed = null_mean = p_value = float("nan")
                used = 0
            else:
                observed, null_mean, p_value, used = stratified_null(
                    values, selected, background, strata, rng
                )
            results.append({
                "bridge_id": bridge["bridge_id"],
                "kind": bridge["kind"],
                "linked_human_genes": bridge["linked_human_genes"],
                "linked_fly_genes": bridge["linked_fly_genes"],
                "fca_cell_type": bridge["fca_cell_type"],
                "direction": direction,
                "annotated_group_neurons": len(group_ids),
                "tested_group_neurons": used,
                "mean_dopamine_weight_fraction": observed,
                "matched_null_mean_fraction": null_mean,
                "fold_vs_matched_null": observed / null_mean if null_mean > 0 else "",
                "group_total_connection_weight": int(total_weight[selected].sum()),
                "group_dopamine_connection_weight": int(dopamine_weight[selected].sum()),
                "group_total_degree": int(degree[selected].sum()),
                "neurons_with_direct_dopamine_connection": int(np.count_nonzero(dopamine_weight[selected] > 0)),
                "empirical_p_one_sided": p_value,
                "fdr_bh": "",
                "permutations": PERMUTATIONS,
                "matching": "anatomical family + total connection strength quintile + degree quintile",
                "null_method": "stratified bootstrap with replacement",
            })

    candidate_indices = [index for index, row in enumerate(results) if row["kind"] == "candidate"]
    p_values = [
        1.0 if not np.isfinite(float(row["empirical_p_one_sided"])) else float(row["empirical_p_one_sided"])
        for row in results
    ]
    adjusted = bh_adjust(candidate_indices, p_values)
    for index, value in adjusted.items():
        results[index]["fdr_bh"] = value

    results.sort(key=lambda row: (
        row["kind"] != "candidate",
        float(row["fdr_bh"]) if row["fdr_bh"] != "" else 2.0,
        row["bridge_id"],
        row["direction"],
    ))

    bridge_path = OUTPUT / "m2b-cell-type-bridges.csv"
    with bridge_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(bridge_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(bridge_rows)

    result_path = OUTPUT / "m2b-dopamine-proximity.csv"
    with result_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    significant = [
        row for row in results
        if row["kind"] == "candidate" and row["fdr_bh"] != "" and float(row["fdr_bh"]) < 0.05
    ]
    summary = {
        "experiment": "M2B curated candidate-cell-type dopamine proximity",
        "annotation_rows": len(ids),
        "connectome_rows_scanned": metrics["rows_scanned"],
        "consensus_dopamine_neurons": len(dopamine_ids),
        "candidate_bridge_groups": sum(row["kind"] == "candidate" for row in bridge_rows),
        "calibration_groups": sum(row["kind"] == "calibration" for row in bridge_rows),
        "candidate_tests": len(candidate_indices),
        "permutations": PERMUTATIONS,
        "random_seed": SEED,
        "significant_candidate_tests_fdr_lt_0_05": [
            {
                "bridge_id": row["bridge_id"],
                "direction": row["direction"],
                "fdr_bh": row["fdr_bh"],
                "fold_vs_matched_null": row["fold_vs_matched_null"],
            }
            for row in significant
        ],
        "boundaries": [
            "Only explicit annotation bridges are tested; unmapped detailed cell types remain unknown.",
            "Fly Cell Atlas expression is not assigned to individual MaleCNS body IDs.",
            "Connectivity proximity is not evidence that the linked gene is expressed in each tested neuron.",
            "The stratified bootstrap treats reconstructed neurons as sampling units and does not prove causality.",
        ],
    }
    with (OUTPUT / "m2b-summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
