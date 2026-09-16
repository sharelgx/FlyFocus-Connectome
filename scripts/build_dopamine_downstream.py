#!/usr/bin/env python3
"""Aggregate direct downstream targets of consensus dopamine MaleCNS neurons."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.feather as feather
import pyarrow.ipc as ipc


ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = ROOT / "data/flat-connectome/connectome-weights-male-cns-v1.0-minconf-0.5.feather"
ANNOTATIONS = ROOT / "data/flat-connectome/body-annotations-male-cns-v1.0-minconf-0.5.feather"
TARGETS = ROOT / "outputs/malecns-dopamine-target-neurons.csv"
OUTPUT = ROOT / "outputs"
TOP_N = 5000

ANNOTATION_FIELDS = [
    "bodyId", "type", "instance", "class", "subclass", "superclass",
    "supertype", "flywireType", "hemibrainType", "mancType", "vfbId",
    "somaSide", "somaNeuromere", "rootSide", "statusLabel", "receptorType",
]


def main():
    with TARGETS.open(encoding="utf-8", newline="") as handle:
        consensus_ids = {
            int(row["bodyId"])
            for row in csv.DictReader(handle)
            if row["dopamine_evidence"] == "consensus_dopamine"
        }
    if not consensus_ids:
        raise RuntimeError("No consensus dopamine body IDs found")

    target_weight = defaultdict(int)
    target_edges = defaultdict(int)
    filtered_edges = 0
    scanned_rows = 0
    with pa.memory_map(str(WEIGHTS), "r") as source:
        reader = ipc.open_file(source)
        id_type = reader.schema.field("body_pre").type
        value_set = pa.array(sorted(consensus_ids), type=id_type)
        for batch_index in range(reader.num_record_batches):
            batch = reader.get_batch(batch_index)
            scanned_rows += batch.num_rows
            mask = pc.is_in(batch["body_pre"], value_set=value_set)
            selected = pc.filter(batch, mask)
            filtered_edges += selected.num_rows
            for post, weight in zip(selected["body_post"].to_pylist(), selected["weight"].to_pylist()):
                target_weight[post] += int(weight)
                target_edges[post] += 1

    annotation_table = feather.read_table(ANNOTATIONS, columns=ANNOTATION_FIELDS)
    posts = pa.array(sorted(target_weight), type=annotation_table.schema.field("bodyId").type)
    selected_annotations = pc.filter(
        annotation_table,
        pc.is_in(annotation_table["bodyId"], value_set=posts),
    )
    annotation_by_body = {row["bodyId"]: row for row in selected_annotations.to_pylist()}

    total_weight = sum(target_weight.values())
    ranked = sorted(target_weight, key=lambda body: (-target_weight[body], body))
    fields = [
        "rank", "bodyId", "consensus_dopamine_input_weight",
        "consensus_dopamine_edge_count", "fraction_of_consensus_dopamine_output",
    ] + [field for field in ANNOTATION_FIELDS if field != "bodyId"]
    rows = []
    for rank, body in enumerate(ranked[:TOP_N], 1):
        result = {
            "rank": rank,
            "bodyId": body,
            "consensus_dopamine_input_weight": target_weight[body],
            "consensus_dopamine_edge_count": target_edges[body],
            "fraction_of_consensus_dopamine_output": target_weight[body] / total_weight if total_weight else 0,
        }
        result.update({key: "" if value is None else value for key, value in annotation_by_body.get(body, {}).items()})
        rows.append(result)
    with (OUTPUT / "malecns-consensus-dopamine-downstream-top5000.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)

    grouped = defaultdict(lambda: {"weight": 0, "targets": set(), "edges": 0})
    for body, weight in target_weight.items():
        annotation = annotation_by_body.get(body, {})
        group = annotation.get("type") or annotation.get("class") or annotation.get("superclass") or "unannotated"
        grouped[group]["weight"] += weight
        grouped[group]["targets"].add(body)
        grouped[group]["edges"] += target_edges[body]
    group_rows = [
        {
            "downstream_group": group,
            "total_weight": values["weight"],
            "target_neurons": len(values["targets"]),
            "consensus_dopamine_edges": values["edges"],
            "fraction_of_consensus_dopamine_output": values["weight"] / total_weight if total_weight else 0,
        }
        for group, values in grouped.items()
    ]
    group_rows.sort(key=lambda row: (-row["total_weight"], row["downstream_group"]))
    with (OUTPUT / "malecns-consensus-dopamine-downstream-groups.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(group_rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(group_rows)

    summary = {
        "consensus_dopamine_source_neurons": len(consensus_ids),
        "connectome_rows_scanned": scanned_rows,
        "direct_edges_found": filtered_edges,
        "unique_downstream_neurons": len(target_weight),
        "total_outgoing_synapse_weight": total_weight,
        "annotated_downstream_neurons": len(annotation_by_body),
        "top_table_rows": len(rows),
        "group_rows": len(group_rows),
        "scope": "one-hop outgoing edges from consensus_nt=dopamine neurons",
    }
    with (OUTPUT / "malecns-consensus-dopamine-downstream-summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
