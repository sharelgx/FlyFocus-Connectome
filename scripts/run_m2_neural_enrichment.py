#!/usr/bin/env python3
"""Run M2A: neural-class enrichment and exploratory candidate prioritization.

The inferential analysis uses the 22 broad Fly Cell Atlas classes. Candidate
genes are compared with expression-matched non-candidate genes in 10,000
deterministic permutations. Detailed adult nervous-system clusters are used
only descriptively because they are not direct MaleCNS bodyId measurements.
"""

from __future__ import annotations

import csv
import gzip
import json
import math
import random
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRIORITY = ROOT / "outputs/adhd-priority-fly-genes.csv"
FCA = ROOT / "data/flybase/FlyCellAtlas_slimmed_gene_expression_fb_2026_02.tsv.gz"
DETAIL = ROOT / "outputs/adhd-adult-nervous-scrna-expression.csv"
OUTPUT = ROOT / "outputs"

NEURAL_CLASSES = [
    "neuron",
    "interneuron",
    "motor_neuron",
    "sensory_neuron",
    "sensory_organ_cell",
    "glial_cell",
]
PERMUTATIONS = 10_000
SEED = 20260916
MATCH_BINS = 50


def truthy(value: str) -> bool:
    return value.strip().lower() == "true"


def parse_fca_value(value: str) -> tuple[float, float]:
    if not value or ":" not in value:
        return 0.0, 0.0
    mean, percent = value.split(":", 1)
    return float(mean or 0), float(percent.rstrip("%") or 0)


def read_fca() -> tuple[list[str], dict[str, dict]]:
    with gzip.open(FCA, "rt", encoding="utf-8", errors="replace", newline="") as handle:
        for line in handle:
            if line.startswith("#") and "\t" in line:
                fields = line.lstrip("#").rstrip("\r\n").split("\t")
                break
        else:
            raise ValueError(f"No header found in {FCA}")

        cell_classes = fields[2:]
        genes = {}
        for row in csv.DictReader(handle, fieldnames=fields, delimiter="\t"):
            gene_id = row["gene_id"]
            means = {}
            percents = {}
            for cell_class in cell_classes:
                means[cell_class], percents[cell_class] = parse_fca_value(row[cell_class])
            genes[gene_id] = {
                "symbol": row["gene_Symbol"],
                "means": means,
                "percents": percents,
            }
    return cell_classes, genes


def load_candidates() -> dict[str, dict]:
    candidates = {}
    with PRIORITY.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            gene_id = row["dmel_gene_id"]
            item = candidates.setdefault(gene_id, {
                "fly_gene_symbol": row["dmel_gene_symbol"],
                "human_gene_symbols": set(),
                "diopt_score": 0,
                "credible_set_mapped": False,
                "magma_exomewide": False,
                "magma_p": None,
                "positive_control": False,
                "flybase_disease_model_count": 0,
            })
            item["human_gene_symbols"].add(row["human_gene_symbol"])
            item["diopt_score"] = max(item["diopt_score"], int(row["diopt_score"] or 0))
            item["credible_set_mapped"] |= truthy(row["credible_set_mapped"])
            item["magma_exomewide"] |= truthy(row["magma_exomewide"])
            item["positive_control"] |= truthy(row["positive_control"])
            item["flybase_disease_model_count"] = max(
                item["flybase_disease_model_count"],
                int(row["flybase_disease_model_count"] or 0),
            )
            if row["magma_p"]:
                p = float(row["magma_p"])
                item["magma_p"] = p if item["magma_p"] is None else min(item["magma_p"], p)
    return candidates


def bh_adjust(p_values: list[float]) -> list[float]:
    order = sorted(range(len(p_values)), key=p_values.__getitem__)
    adjusted = [1.0] * len(p_values)
    running = 1.0
    n = len(p_values)
    for rank_index in range(n - 1, -1, -1):
        index = order[rank_index]
        rank = rank_index + 1
        running = min(running, p_values[index] * n / rank)
        adjusted[index] = running
    return adjusted


def evidence_tier(item: dict) -> tuple[str, float]:
    credible = item["credible_set_mapped"]
    magma = item["magma_exomewide"]
    if credible and magma:
        return "credible_set_and_magma", 35.0
    if credible:
        return "credible_set", 25.0
    if magma:
        return "magma", 22.0
    return "literature_positive_control", 15.0


def build_enrichment(candidate_ids: list[str], genes: dict[str, dict]) -> list[dict]:
    expressed_ids = [
        gene_id for gene_id, gene in genes.items()
        if any(gene["percents"].values())
    ]
    ordered = sorted(
        expressed_ids,
        key=lambda gene_id: (
            sum(genes[gene_id]["percents"][name] for name in NEURAL_CLASSES) / len(NEURAL_CLASSES),
            gene_id,
        ),
    )
    bins = {
        gene_id: min(MATCH_BINS - 1, index * MATCH_BINS // len(ordered))
        for index, gene_id in enumerate(ordered)
    }
    candidate_set = set(candidate_ids)
    background_by_bin = defaultdict(list)
    candidate_count_by_bin = defaultdict(int)
    for gene_id in ordered:
        if gene_id in candidate_set:
            candidate_count_by_bin[bins[gene_id]] += 1
        else:
            background_by_bin[bins[gene_id]].append(gene_id)

    for bin_id, count in candidate_count_by_bin.items():
        if len(background_by_bin[bin_id]) < count:
            raise RuntimeError(f"Insufficient matched background genes in bin {bin_id}")

    observed = {
        name: sum(genes[gene_id]["percents"][name] for gene_id in candidate_ids) / len(candidate_ids)
        for name in NEURAL_CLASSES
    }
    null_sum = {name: 0.0 for name in NEURAL_CLASSES}
    exceed = {name: 0 for name in NEURAL_CLASSES}
    rng = random.Random(SEED)
    for _ in range(PERMUTATIONS):
        sampled = []
        for bin_id, count in candidate_count_by_bin.items():
            sampled.extend(rng.sample(background_by_bin[bin_id], count))
        for name in NEURAL_CLASSES:
            value = sum(genes[gene_id]["percents"][name] for gene_id in sampled) / len(sampled)
            null_sum[name] += value
            if value >= observed[name]:
                exceed[name] += 1

    p_values = [(exceed[name] + 1) / (PERMUTATIONS + 1) for name in NEURAL_CLASSES]
    fdr_values = bh_adjust(p_values)
    rows = []
    for index, name in enumerate(NEURAL_CLASSES):
        null_mean = null_sum[name] / PERMUTATIONS
        rows.append({
            "cell_class": name,
            "candidate_genes": len(candidate_ids),
            "candidate_mean_positive_percent": observed[name],
            "matched_null_mean_positive_percent": null_mean,
            "difference_percentage_points": observed[name] - null_mean,
            "empirical_p_one_sided": p_values[index],
            "fdr_bh": fdr_values[index],
            "permutations": PERMUTATIONS,
            "matching_variable": (
                f"mean positive percent across six neural classes; {MATCH_BINS}-quantile matched"
            ),
        })
    rows.sort(key=lambda row: (row["fdr_bh"], -row["difference_percentage_points"]))
    return rows


def build_priority(candidates: dict[str, dict], genes: dict[str, dict], cell_classes: list[str]) -> list[dict]:
    non_neural = [name for name in cell_classes if name not in NEURAL_CLASSES]
    rows = []
    for gene_id, item in candidates.items():
        if gene_id not in genes:
            continue
        gene = genes[gene_id]
        neural_mean = sum(gene["percents"][name] for name in NEURAL_CLASSES) / len(NEURAL_CLASSES)
        non_neural_mean = sum(gene["percents"][name] for name in non_neural) / len(non_neural)
        specificity = neural_mean - non_neural_mean
        tier, evidence_points = evidence_tier(item)
        orthology_points = 25 * min(item["diopt_score"] / 15, 1)
        neural_points = 20 * min(neural_mean / 75, 1)
        specificity_points = 10 * min(max(specificity, 0) / 30, 1)
        disease_points = 10 * min(item["flybase_disease_model_count"] / 2, 1)
        score = evidence_points + orthology_points + neural_points + specificity_points + disease_points
        rows.append({
            "rank": 0,
            "human_gene_symbols": " | ".join(sorted(item["human_gene_symbols"])),
            "dmel_gene_id": gene_id,
            "dmel_gene_symbol": item["fly_gene_symbol"],
            "evidence_tier": tier,
            "credible_set_mapped": item["credible_set_mapped"],
            "magma_exomewide": item["magma_exomewide"],
            "magma_p": "" if item["magma_p"] is None else item["magma_p"],
            "positive_control": item["positive_control"],
            "diopt_score": item["diopt_score"],
            "flybase_disease_model_count": item["flybase_disease_model_count"],
            "mean_neural_positive_percent": neural_mean,
            "mean_non_neural_positive_percent": non_neural_mean,
            "neural_specificity_percentage_points": specificity,
            "exploratory_priority_score_0_100": score,
            "score_boundary": "heuristic ranking, not a probability or statistical significance",
        })
    rows.sort(key=lambda row: (-row["exploratory_priority_score_0_100"], row["dmel_gene_symbol"]))
    for rank, row in enumerate(rows, 1):
        row["rank"] = rank
    return rows


def build_detailed_highlights(candidate_ids: set[str]) -> list[dict]:
    by_gene_cell = {}
    with DETAIL.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            gene_id = row["Gene_ID"]
            if gene_id not in candidate_ids:
                continue
            key = (gene_id, row["Cluster_Cell_Type_ID"], row["Cluster_Cell_Type_Name"])
            current = by_gene_cell.get(key)
            spread = float(row["Spread"] or 0)
            mean_expression = float(row["Mean_Expression"] or 0)
            if current is None:
                by_gene_cell[key] = {
                    "human_gene_symbols": row["human_gene_symbols"],
                    "dmel_gene_id": gene_id,
                    "dmel_gene_symbol": row["Gene_Symbol"],
                    "cell_type_id": row["Cluster_Cell_Type_ID"],
                    "cell_type_name": row["Cluster_Cell_Type_Name"],
                    "max_spread": spread,
                    "max_mean_expression": mean_expression,
                    "supporting_rows": 1,
                }
            else:
                current["max_spread"] = max(current["max_spread"], spread)
                current["max_mean_expression"] = max(current["max_mean_expression"], mean_expression)
                current["supporting_rows"] += 1

    by_gene = defaultdict(list)
    for row in by_gene_cell.values():
        by_gene[row["dmel_gene_id"]].append(row)
    highlights = []
    for gene_rows in by_gene.values():
        gene_rows.sort(key=lambda row: (-row["max_spread"], -row["max_mean_expression"], row["cell_type_name"]))
        for rank, row in enumerate(gene_rows[:5], 1):
            row["within_gene_rank"] = rank
            highlights.append(row)
    highlights.sort(key=lambda row: (row["dmel_gene_symbol"], row["within_gene_rank"]))
    return highlights


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise RuntimeError(f"No rows generated for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    candidates = load_candidates()
    cell_classes, genes = read_fca()
    candidate_ids = sorted(gene_id for gene_id in candidates if gene_id in genes)

    enrichment = build_enrichment(candidate_ids, genes)
    priority = build_priority(candidates, genes, cell_classes)
    highlights = build_detailed_highlights(set(candidate_ids))

    write_csv(OUTPUT / "m2-neural-cell-class-enrichment.csv", enrichment)
    write_csv(OUTPUT / "m2-candidate-priority.csv", priority)
    write_csv(OUTPUT / "m2-candidate-cell-type-highlights.csv", highlights)

    novel_priority = [row for row in priority if not row["positive_control"]]
    significant = [row for row in enrichment if row["fdr_bh"] < 0.05]
    summary = {
        "experiment": "M2A neural-class enrichment and candidate prioritization",
        "candidate_priority_rows": len(priority),
        "unique_priority_fly_genes_tested": len(candidate_ids),
        "background_fca_genes": len(genes),
        "permutations": PERMUTATIONS,
        "random_seed": SEED,
        "significant_neural_classes_fdr_lt_0_05": [row["cell_class"] for row in significant],
        "top_novel_candidates": [
            {
                "rank": row["rank"],
                "human": row["human_gene_symbols"],
                "fly": row["dmel_gene_symbol"],
                "score": row["exploratory_priority_score_0_100"],
            }
            for row in novel_priority[:10]
        ],
        "boundaries": [
            "The priority score is an explicit exploratory heuristic, not a probability or p-value.",
            "Broad-class enrichment is expression-matched but does not establish causality.",
            "Detailed FlyBase cell types are not direct MaleCNS bodyId measurements.",
            "No gene-to-bodyId assignment is made in M2A.",
        ],
    }
    with (OUTPUT / "m2-summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
