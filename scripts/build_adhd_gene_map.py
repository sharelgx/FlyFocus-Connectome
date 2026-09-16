#!/usr/bin/env python3
"""Build a source-traceable ADHD-to-Drosophila gene and expression map.

The script intentionally stops at FlyBase cell types.  It does not claim that
single-cell clusters map directly to individual MaleCNS body IDs.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

import openpyxl


ROOT = Path(__file__).resolve().parents[1]
GWAS = ROOT / "data/human-adhd/41588_2022_1285_MOESM6_ESM.xlsx"
ORTHOLOGS = ROOT / "data/flybase/dmel_human_orthologs_disease_fb_2026_02.tsv.gz"
DISEASE_MODELS = ROOT / "data/flybase/human_disease_models_fb_2026_02.tsv.gz"
FCA_SLIM = ROOT / "data/flybase/FlyCellAtlas_slimmed_gene_expression_fb_2026_02.tsv.gz"
SCRNA = ROOT / "data/flybase/scRNA-Seq_gene_expression_fb_2026_02.tsv.gz"
OUTPUT = ROOT / "outputs"

POSITIVE_CONTROLS = {
    "SLC6A3": "DAT dopamine-transporter literature control",
    "ADGRL3": "latrophilin literature control",
    "NF1": "NF1 literature control",
    "MEF2C": "locomotor/sleep literature control",
    "TRAPPC9": "locomotor/sleep literature control",
}

NERVOUS_TERMS = (
    "brain",
    "head",
    "nervous",
    "optic lobe",
    "ventral nerve cord",
    "ganglion",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def clean(value):
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.15g}"
    return str(value).strip()


def usable_symbol(value: str) -> bool:
    return bool(value and value.upper() not in {"NA", "N/A", "NULL", "NONE"})


def read_xlsx_table(ws, header_row: int):
    rows = ws.iter_rows(min_row=header_row, values_only=True)
    headers = [clean(value) for value in next(rows)]
    for values in rows:
        row = {headers[i]: clean(value) for i, value in enumerate(values) if i < len(headers) and headers[i]}
        if any(row.values()):
            yield row


def read_gzip_tsv(path: Path):
    with gzip.open(path, "rt", encoding="utf-8", errors="replace", newline="") as handle:
        for line in handle:
            # FlyBase files use either one or two leading hashes for the real
            # tab-separated header; prose comment lines contain no tabs.
            if line.startswith("#") and "\t" in line:
                header = line.lstrip("#").rstrip("\n\r").split("\t")
                break
        else:
            raise ValueError(f"No TSV header found in {path}")
        yield from csv.DictReader(handle, fieldnames=header, delimiter="\t")


def write_csv(path: Path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def parse_expression(value: str):
    if not value or ":" not in value:
        return "", ""
    mean, percent = value.split(":", 1)
    return mean, percent.rstrip("%")


def tokens(value: str):
    return set(re.findall(r"(?:FBgn\d+|[A-Za-z][A-Za-z0-9_.-]+)", value or ""))


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.load_workbook(GWAS, read_only=True, data_only=True)
    candidates = defaultdict(lambda: {
        "credible_set_mapped": False,
        "magma_exomewide": False,
        "positive_control": False,
        "magma_p": "",
        "sources": set(),
    })

    for row in read_xlsx_table(wb["7.Genes mapped by crediblesets"], 4):
        # Some supplementary rows use the literal string "NA" in HUGO even
        # though the source symbol column is populated.  Treat it as missing,
        # not as a real human gene symbol.
        symbol = row.get("HUGO", "")
        if not usable_symbol(symbol):
            symbol = row.get("symbol", "")
        if symbol:
            candidates[symbol]["credible_set_mapped"] = True
            candidates[symbol]["sources"].add("Demontis2023_Table7")

    for row in read_xlsx_table(wb["13. Magma genes"], 2):
        symbol = row.get("SYMBOL")
        if symbol:
            candidates[symbol]["magma_exomewide"] = True
            candidates[symbol]["magma_p"] = row.get("P", "")
            candidates[symbol]["sources"].add("Demontis2023_Table13")

    for symbol, note in POSITIVE_CONTROLS.items():
        candidates[symbol]["positive_control"] = True
        candidates[symbol]["sources"].add(note)

    candidate_rows = []
    for symbol in sorted(candidates):
        item = candidates[symbol]
        candidate_rows.append({
            "human_gene_symbol": symbol,
            "credible_set_mapped": item["credible_set_mapped"],
            "magma_exomewide": item["magma_exomewide"],
            "magma_p": item["magma_p"],
            "positive_control": item["positive_control"],
            "evidence_sources": " | ".join(sorted(item["sources"])),
        })
    write_csv(
        OUTPUT / "adhd-human-candidate-genes.csv",
        candidate_rows,
        list(candidate_rows[0]),
    )

    ortholog_rows = []
    for row in read_gzip_tsv(ORTHOLOGS):
        human = row.get("Human_gene_symbol", "")
        if human in candidates:
            ortholog_rows.append({
                "human_gene_symbol": human,
                "dmel_gene_id": row.get("Dmel_gene_ID", ""),
                "dmel_gene_symbol": row.get("Dmel_gene_symbol", ""),
                "diopt_score": row.get("DIOPT_score", ""),
                "hgnc_id": row.get("Human_gene_HGNC_ID", ""),
                "omim_gene_id": row.get("Human_gene_OMIM_ID", ""),
                "omim_phenotype_ids": row.get("OMIM_Phenotype_IDs", ""),
                "ortholog_source": "FlyBase_FB2026_02",
            })

    by_human = defaultdict(list)
    for row in ortholog_rows:
        by_human[row["human_gene_symbol"]].append(row)
    for human, rows in by_human.items():
        scores = [int(r["diopt_score"]) for r in rows if r["diopt_score"].isdigit()]
        maximum = max(scores) if scores else None
        for row in rows:
            row["top_diopt_for_human_gene"] = bool(
                maximum is not None and row["diopt_score"].isdigit() and int(row["diopt_score"]) == maximum
            )

    for human in sorted(candidates):
        if human not in by_human:
            ortholog_rows.append({
                "human_gene_symbol": human,
                "dmel_gene_id": "",
                "dmel_gene_symbol": "",
                "diopt_score": "",
                "hgnc_id": "",
                "omim_gene_id": "",
                "omim_phenotype_ids": "",
                "ortholog_source": "FlyBase_FB2026_02_no_match",
                "top_diopt_for_human_gene": False,
            })
    ortholog_rows.sort(key=lambda r: (r["human_gene_symbol"], -int(r["diopt_score"] or -1), r["dmel_gene_symbol"]))

    fly_to_human = defaultdict(set)
    for row in ortholog_rows:
        if row["dmel_gene_id"]:
            fly_to_human[row["dmel_gene_id"]].add(row["human_gene_symbol"])

    disease_by_human = defaultdict(set)
    disease_by_fly = defaultdict(set)
    for row in read_gzip_tsv(DISEASE_MODELS):
        disease_id = row.get("FB_id", "")
        human_tokens = tokens(row.get("implicated_human_gene", ""))
        fly_tokens = tokens(row.get("implicated_Dmel_gene", ""))
        for human in human_tokens & candidates.keys():
            disease_by_human[human].add(disease_id)
        for fly in fly_tokens & fly_to_human.keys():
            disease_by_fly[fly].add(disease_id)

    for row in ortholog_rows:
        ids = disease_by_human[row["human_gene_symbol"]] | disease_by_fly[row["dmel_gene_id"]]
        row["flybase_disease_model_count"] = len(ids)
        row["flybase_disease_model_ids"] = " | ".join(sorted(ids))

    ortholog_fields = [
        "human_gene_symbol", "dmel_gene_id", "dmel_gene_symbol", "diopt_score",
        "top_diopt_for_human_gene", "hgnc_id", "omim_gene_id", "omim_phenotype_ids",
        "flybase_disease_model_count", "flybase_disease_model_ids", "ortholog_source",
    ]
    write_csv(OUTPUT / "adhd-human-fly-orthologs.csv", ortholog_rows, ortholog_fields)

    relevant_cell_types = [
        "neuron", "interneuron", "motor_neuron", "sensory_neuron",
        "sensory_organ_cell", "glial_cell",
    ]
    slim_rows = []
    for row in read_gzip_tsv(FCA_SLIM):
        fly_id = row.get("gene_id", "")
        if fly_id not in fly_to_human:
            continue
        result = {
            "human_gene_symbols": " | ".join(sorted(fly_to_human[fly_id])),
            "dmel_gene_id": fly_id,
            "dmel_gene_symbol": row.get("gene_Symbol", ""),
        }
        for cell_type in relevant_cell_types:
            mean, percent = parse_expression(row.get(cell_type, ""))
            result[f"{cell_type}_mean_expression"] = mean
            result[f"{cell_type}_positive_percent"] = percent
        slim_rows.append(result)
    slim_rows.sort(key=lambda r: (r["human_gene_symbols"], r["dmel_gene_symbol"]))
    slim_fields = list(slim_rows[0]) if slim_rows else ["human_gene_symbols", "dmel_gene_id", "dmel_gene_symbol"]
    write_csv(OUTPUT / "adhd-flycellatlas-expression-summary.csv", slim_rows, slim_fields)

    slim_by_fly = {row["dmel_gene_id"]: row for row in slim_rows}
    priority_rows = []
    for row in ortholog_rows:
        if not row["dmel_gene_id"] or not row["top_diopt_for_human_gene"]:
            continue
        evidence = candidates[row["human_gene_symbol"]]
        expression = slim_by_fly.get(row["dmel_gene_id"], {})
        priority = {
            "human_gene_symbol": row["human_gene_symbol"],
            "dmel_gene_id": row["dmel_gene_id"],
            "dmel_gene_symbol": row["dmel_gene_symbol"],
            "diopt_score": row["diopt_score"],
            "credible_set_mapped": evidence["credible_set_mapped"],
            "magma_exomewide": evidence["magma_exomewide"],
            "magma_p": evidence["magma_p"],
            "positive_control": evidence["positive_control"],
            "flybase_disease_model_count": row["flybase_disease_model_count"],
        }
        for field, value in expression.items():
            if field.endswith("_mean_expression") or field.endswith("_positive_percent"):
                priority[field] = value
        priority_rows.append(priority)
    priority_rows.sort(key=lambda r: (r["human_gene_symbol"], r["dmel_gene_symbol"]))
    priority_fields = list(priority_rows[0]) if priority_rows else ["human_gene_symbol", "dmel_gene_id"]
    write_csv(OUTPUT / "adhd-priority-fly-genes.csv", priority_rows, priority_fields)

    detailed_path = OUTPUT / "adhd-adult-nervous-scrna-expression.csv"
    detailed_fields = [
        "human_gene_symbols", "Pub_ID", "Pub_miniref", "Clustering_Analysis_ID",
        "Clustering_Analysis_Name", "Source_Tissue_Sex", "Source_Tissue_Stage",
        "Source_Tissue_Anatomy", "Cluster_ID", "Cluster_Name", "Cluster_Cell_Type_ID",
        "Cluster_Cell_Type_Name", "Gene_ID", "Gene_Symbol", "Mean_Expression", "Spread",
    ]
    scanned = 0
    kept = 0
    with detailed_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=detailed_fields, lineterminator="\n")
        writer.writeheader()
        for row in read_gzip_tsv(SCRNA):
            scanned += 1
            fly_id = row.get("Gene_ID", "")
            if fly_id not in fly_to_human:
                continue
            if row.get("Source_Tissue_Stage") != "adult stage":
                continue
            context = " ".join((
                row.get("Source_Tissue_Anatomy", ""),
                row.get("Cluster_Cell_Type_Name", ""),
                row.get("Cluster_Name", ""),
            )).lower()
            if not any(term in context for term in NERVOUS_TERMS) and not re.search(r"neuron|glia", context):
                continue
            output = {field: row.get(field, "") for field in detailed_fields}
            output["human_gene_symbols"] = " | ".join(sorted(fly_to_human[fly_id]))
            writer.writerow(output)
            kept += 1
            if scanned % 5_000_000 == 0:
                print(f"scRNA rows scanned={scanned:,}, kept={kept:,}", flush=True)

    source_files = [GWAS, ORTHOLOGS, DISEASE_MODELS, FCA_SLIM, SCRNA]
    summary = {
        "method": "Demontis 2023 Tables 7 and 13 union plus literature positive controls; FlyBase FB2026_02 joins",
        "human_candidate_genes": len(candidates),
        "credible_set_genes": sum(bool(v["credible_set_mapped"]) for v in candidates.values()),
        "magma_genes": sum(bool(v["magma_exomewide"]) for v in candidates.values()),
        "positive_controls": len(POSITIVE_CONTROLS),
        "human_genes_with_flybase_ortholog": len(by_human),
        "human_genes_without_flybase_ortholog": len(candidates) - len(by_human),
        "ortholog_rows": sum(bool(r["dmel_gene_id"]) for r in ortholog_rows),
        "unique_dmel_genes": len(fly_to_human),
        "flycellatlas_summary_rows": len(slim_rows),
        "top_diopt_priority_rows": len(priority_rows),
        "scrna_rows_scanned": scanned,
        "adult_nervous_scrna_rows_kept": kept,
        "direct_body_id_mapping": False,
        "mapping_boundary": "FlyBase cell clusters are not direct MaleCNS bodyId measurements",
        "source_files": [
            {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in source_files
        ],
    }
    with (OUTPUT / "adhd-mapping-summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
