# ADHD reference-data provenance

Downloaded and verified on 2026-09-16. All paths are relative to the project
root. SHA-256 values are stored in `SHA256SUMS` in this directory.

| Local file | Bytes | Release/source |
| --- | ---: | --- |
| `data/human-adhd/41588_2022_1285_MOESM6_ESM.xlsx` | 9,081,487 | Demontis et al. 2023 supplementary tables |
| `data/flybase/dmel_human_orthologs_disease_fb_2026_02.tsv.gz` | 764,088 | FlyBase FB2026_02 |
| `data/flybase/human_disease_models_fb_2026_02.tsv.gz` | 1,413,698 | FlyBase FB2026_02 |
| `data/flybase/FlyCellAtlas_slimmed_gene_expression_fb_2026_02.tsv.gz` | 914,253 | FlyBase FB2026_02 / Fly Cell Atlas |
| `data/flybase/scRNA-Seq_gene_expression_fb_2026_02.tsv.gz` | 514,548,344 | FlyBase FB2026_02 |

The FlyBase files were downloaded from the official public AWS Open Data
bucket (`s3://s3ftp.flybase.org`) through its unsigned HTTPS endpoint because
the human-facing CloudFront domain returned an automated-request challenge.
The object names and byte lengths match the files linked from the FlyBase
FB2026_02 current-release page.

Primary source pages:

- <https://www.nature.com/articles/s41588-022-01285-8>
- <https://flybase.org/downloads/bulkdata>
- <https://wiki.flybase.org/wiki/FlyBase:FilesOverview>
- <https://flycellatlas.org/>
