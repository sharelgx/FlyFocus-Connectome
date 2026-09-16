# Milestone M1: Human ADHD candidates to Drosophila ortholog map

Date: 2026-09-16
Release marker: `v0.1.0`
Status: complete within the mapping and first-pass expression scope

## Outcome

FlyFocus Connectome now has a reproducible bridge from published human ADHD
genetic evidence to prioritized Drosophila ortholog candidates:

```text
Demontis 2023 ADHD evidence
  -> 107 source-traceable candidate/control records
  -> FlyBase FB2026_02 ortholog mapping
  -> 74 mapped human genes
  -> 177 human-fly relationships
  -> 149 distinct Drosophila genes
  -> 79 highest-DIOPT priority mappings, including ties
```

The 107 records are the union of 76 credible-set mapped genes, 45 MAGMA genes,
and five literature positive controls; the categories overlap. Four controls
(`ADGRL3`, `NF1`, `SLC6A3`, `TRAPPC9`) are positive-control-only records, while
`MEF2C` is also present in the MAGMA result.

The supplementary-table parser treats literal `NA` values as missing gene
symbols and falls back to the source `symbol` field. This preserves the source
record `ENSG00000228008 / CTD-2330K9.3` without inventing a human gene named
`NA`.

## Reproducible artifacts

- `scripts/build_adhd_gene_map.py`
- `outputs/adhd-human-candidate-genes.csv`
- `outputs/adhd-human-fly-orthologs.csv`
- `outputs/adhd-priority-fly-genes.csv`
- `outputs/adhd-flycellatlas-expression-summary.csv`
- `outputs/adhd-mapping-summary.json`
- `metadata/adhd/SOURCES.md`
- `metadata/adhd/SHA256SUMS`

The large adult nervous-system single-cell expression table remains local and
is reproducible from the documented FlyBase source.

## Validation

The five expected literature controls map to the anticipated top fly genes:

| Human | Drosophila | DIOPT |
| --- | --- | ---: |
| `SLC6A3` | `DAT` | 12 |
| `ADGRL3` | `Cirl` | 10 |
| `NF1` | `Nf1` | 14 |
| `MEF2C` | `Mef2` | 11 |
| `TRAPPC9` | `brun` | 13 |

This is a pipeline sanity check, not independent evidence that every candidate
causes ADHD.

## Prior art and novelty boundary

This project does **not** claim to be the first use of Drosophila for ADHD or
the first human-to-fly ortholog mapping. Prior work includes:

- dopamine-related locomotor phenotypes for `DAT1`, `LPHN3`, and `NF1` orthologs:
  <https://pubmed.ncbi.nlm.nih.gov/25962619/>
- a high-throughput behavioral screen of 14 ADHD candidate genes:
  <https://pubmed.ncbi.nlm.nih.gov/26954609/>
- activity and sleep experiments for `MEF2C` and `TRAPPC9` orthologs:
  <https://pubmed.ncbi.nlm.nih.gov/32046534/>
- single-cell responses to methylphenidate and atomoxetine in the fly brain:
  <https://pubmed.ncbi.nlm.nih.gov/37957291/>
- general DIOPT human-fly ortholog mapping:
  <https://pubmed.ncbi.nlm.nih.gov/21880147/>

A search of PubMed, bioRxiv, medRxiv, and public GitHub repositories on
2026-09-16 did not identify an equivalent public pipeline combining the
Demontis 2023 ADHD gene set, FlyBase FB2026_02 orthology, adult nervous-system
single-cell expression, and MaleCNS v1.0 circuit analysis. This supports a
**combination-novelty / early-public-implementation** claim, not a global
exclusivity claim. Absence from these searches is not proof that no unpublished
or differently indexed work exists.

## Scientific boundary and next gate

Orthology prioritizes experiments; it does not prove conserved function or ADHD
causality. The next publishable gate is to test whether prioritized genes are
enriched in specific adult neural cell classes and whether their candidate
circuits show robust, null-model-controlled concentration in dopamine,
mushroom-body, sleep, and attention-like networks in MaleCNS.
