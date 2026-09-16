#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
human_dir="$project_dir/data/human-adhd"
flybase_dir="$project_dir/data/flybase"

mkdir -p "$human_dir" "$flybase_dir"

download() {
  local url="$1"
  local directory="$2"
  local filename="$3"
  if command -v aria2c >/dev/null 2>&1; then
    aria2c \
      --continue=true \
      --max-connection-per-server=8 \
      --split=8 \
      --min-split-size=1M \
      --file-allocation=none \
      --dir="$directory" \
      --out="$filename" \
      "$url"
  else
    curl --fail --location --continue-at - \
      --output "$directory/$filename" \
      "$url"
  fi
}

download \
  "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41588-022-01285-8/MediaObjects/41588_2022_1285_MOESM6_ESM.xlsx" \
  "$human_dir" \
  "41588_2022_1285_MOESM6_ESM.xlsx"

flybase_root="https://s3.amazonaws.com/s3ftp.flybase.org/releases/FB2026_02/precomputed_files"

download \
  "$flybase_root/orthologs/dmel_human_orthologs_disease_fb_2026_02.tsv.gz" \
  "$flybase_dir" \
  "dmel_human_orthologs_disease_fb_2026_02.tsv.gz"

download \
  "$flybase_root/human_disease/human_disease_models_fb_2026_02.tsv.gz" \
  "$flybase_dir" \
  "human_disease_models_fb_2026_02.tsv.gz"

download \
  "$flybase_root/genes/FlyCellAtlas_slimmed_gene_expression_fb_2026_02.tsv.gz" \
  "$flybase_dir" \
  "FlyCellAtlas_slimmed_gene_expression_fb_2026_02.tsv.gz"

download \
  "$flybase_root/genes/scRNA-Seq_gene_expression_fb_2026_02.tsv.gz" \
  "$flybase_dir" \
  "scRNA-Seq_gene_expression_fb_2026_02.tsv.gz"

cd "$project_dir"
shasum -a 256 -c metadata/adhd/SHA256SUMS
