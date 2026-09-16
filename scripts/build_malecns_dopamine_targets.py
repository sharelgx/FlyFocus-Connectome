#!/usr/bin/env python3
"""Create the first direct MaleCNS body-ID target table for the dopamine axis."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import pyarrow.compute as pc
import pyarrow.feather as feather


ROOT = Path(__file__).resolve().parents[1]
NT_PATH = ROOT / "data/flat-connectome/body-neurotransmitters-male-cns-v1.0.feather"
ANN_PATH = ROOT / "data/flat-connectome/body-annotations-male-cns-v1.0-minconf-0.5.feather"
OUTPUT = ROOT / "outputs"

ANNOTATION_FIELDS = [
    "bodyId", "type", "instance", "class", "subclass", "superclass",
    "supertype", "flywireType", "hemibrainType", "mancType", "vfbId",
    "somaSide", "somaNeuromere", "rootSide", "statusLabel", "receptorType",
]


def clean(value):
    return "" if value is None else value


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    nt = feather.read_table(NT_PATH)

    predicted = pc.equal(nt["predicted_nt"], "dopamine")
    celltype = pc.equal(nt["celltype_predicted_nt"], "dopamine")
    consensus = pc.equal(nt["consensus_nt"], "dopamine")
    selected = pc.or_kleene(pc.or_kleene(predicted, celltype), consensus)
    dopamine = pc.filter(nt, selected)
    body_ids = set(dopamine["body"].to_pylist())

    annotations = feather.read_table(ANN_PATH, columns=ANNOTATION_FIELDS)
    annotated = pc.filter(
        annotations,
        pc.is_in(annotations["bodyId"], value_set=dopamine["body"].combine_chunks()),
    )
    annotation_by_body = {row["bodyId"]: row for row in annotated.to_pylist()}

    fields = [
        "bodyId", "dopamine_evidence", "consensus_nt", "predicted_nt",
        "predicted_nt_confidence", "celltype_predicted_nt",
        "celltype_predicted_nt_confidence", "cell_type",
    ] + [field for field in ANNOTATION_FIELDS if field != "bodyId"]

    rows = []
    for source in dopamine.to_pylist():
        if source["consensus_nt"] == "dopamine":
            evidence = "consensus_dopamine"
        elif source["celltype_predicted_nt"] == "dopamine":
            evidence = "celltype_prediction_only"
        else:
            evidence = "individual_prediction_only"
        result = {
            "bodyId": source["body"],
            "dopamine_evidence": evidence,
            "consensus_nt": clean(source["consensus_nt"]),
            "predicted_nt": clean(source["predicted_nt"]),
            "predicted_nt_confidence": clean(source["predicted_nt_confidence"]),
            "celltype_predicted_nt": clean(source["celltype_predicted_nt"]),
            "celltype_predicted_nt_confidence": clean(source["celltype_predicted_nt_confidence"]),
            "cell_type": clean(source["cell_type"]),
        }
        result.update({key: clean(value) for key, value in annotation_by_body.get(source["body"], {}).items()})
        rows.append(result)

    order = {
        "consensus_dopamine": 0,
        "celltype_prediction_only": 1,
        "individual_prediction_only": 2,
    }
    rows.sort(key=lambda row: (order[row["dopamine_evidence"]], str(row.get("type", "")), row["bodyId"]))
    with (OUTPUT / "malecns-dopamine-target-neurons.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "neurotransmitter_records": nt.num_rows,
        "dopamine_target_neurons": len(rows),
        "unique_body_ids": len(body_ids),
        "evidence_counts": dict(Counter(row["dopamine_evidence"] for row in rows)),
        "with_body_annotation": sum(row["bodyId"] in annotation_by_body for row in rows),
        "with_named_type": sum(bool(row.get("type")) for row in rows),
        "boundary": "Dopamine identity is predicted/consensus neurotransmitter evidence, not gene expression measured for each bodyId.",
    }
    with (OUTPUT / "malecns-dopamine-target-summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
