# FlyFocus Connectome

**果蝇注意力回路计划** — exploring attention-, activity-, sleep-, and
dopamine-related neural circuits using the MaleCNS connectome.

GitHub: <https://github.com/sharelgx/FlyFocus-Connectome>

This project contains the three MaleCNS v1.0 flat-connectome tables recommended
for building a simplified neural-network simulation. Large synapse-coordinate,
synapse-partner, EM, and other full-release assets are intentionally not included.

ADHD is used here as a source of human genetic hypotheses and measurable
endophenotypes. This project does not claim that a fruit fly is a complete model
of human ADHD and is not intended for diagnosis or treatment advice.

## Current milestone

**M1 / v0.1.0 — Human ADHD candidates to Drosophila ortholog map**

- 107 source-traceable human candidate/control records
- 74 human genes with FlyBase ortholog relationships
- 177 ortholog rows covering 149 distinct Drosophila genes
- 79 highest-DIOPT priority mappings, including ties
- adult nervous-system expression summaries for all 149 mapped fly genes

The milestone is complete within the mapping scope and reproducible from the
committed scripts and source manifests. It is a prioritization resource, not a
claim that all mapped genes are causal for ADHD or functionally conserved in the
same neural context. See
[`research/MILESTONE-001-adhd-to-drosophila-ortholog-map.md`](research/MILESTONE-001-adhd-to-drosophila-ortholog-map.md).

## M2 in progress

M2A tests whether the 75 unique highest-DIOPT fly genes are enriched in six
broad Fly Cell Atlas neural classes relative to expression-matched background
genes. Ten thousand matched permutations found no class significant after FDR
correction. This supports moving to finer, evidence-backed cell types and
MaleCNS circuit tests rather than claiming generic neural enrichment.

M2B then tests 11 explicitly bridged candidate cell types against the complete
1.1 GB MaleCNS connection-weight graph. After 22 directed tests and FDR
correction, two exploratory signals remain: elevated consensus-dopamine input
to the `FoxP`-linked LC10c group, and elevated TmY4 output to consensus-dopamine
neurons for the `Lar`-linked hypothesis. These are circuit-proximity results,
not body-level gene-expression or causal ADHD claims.

See
[`research/2026-09-16-m2a-neural-enrichment-results.md`](research/2026-09-16-m2a-neural-enrichment-results.md)
and
[`research/2026-09-16-m2b-dopamine-proximity-results.md`](research/2026-09-16-m2b-dopamine-proximity-results.md).
Run:

```bash
.venv/bin/python scripts/run_m2_neural_enrichment.py
.venv/bin/python scripts/run_m2b_dopamine_proximity.py
```

## Project layout

```text
.
├── data/flat-connectome/
│   ├── body-annotations-male-cns-v1.0-minconf-0.5.feather
│   ├── body-neurotransmitters-male-cns-v1.0.feather
│   └── connectome-weights-male-cns-v1.0-minconf-0.5.feather
├── metadata/
│   └── SHA256SUMS
├── research/
│   ├── 2026-09-16-adhd-data-sources.md
│   ├── 2026-09-16-adhd-first-mapping-results.md
│   ├── MILESTONE-001-adhd-to-drosophila-ortholog-map.md
│   └── 2026-09-16-malecns-internet-project-catalog.md
├── requirements.txt
└── README.md
```

All project data, Python dependencies, and generated metadata are kept inside
this project directory. The local Python environment is `.venv/`.
Large scientific tables are excluded from Git; they remain on the project drive
and can be verified using the committed checksums and metadata.

## Sources

- Project: <https://male-cns.janelia.org/>
- Official download page: <https://male-cns.janelia.org/download/>
- Neuron annotations: <https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/body-annotations-male-cns-v1.0-minconf-0.5.feather>
- Neurotransmitter predictions: <https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/body-neurotransmitters-male-cns-v1.0.feather>
- Connection weights: <https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/connectome-weights-male-cns-v1.0-minconf-0.5.feather>

MaleCNS data is provided under CC BY. Cite and attribute the MaleCNS project in
derived work; consult the official site for the preferred citation wording.

## Reading the tables

```bash
source .venv/bin/activate
python - <<'PY'
import pyarrow.feather as feather

path = "data/flat-connectome/body-annotations-male-cns-v1.0-minconf-0.5.feather"
annotations = feather.read_table(path)
print(annotations.shape)
print(annotations.slice(0, 5).to_pylist())
PY
```

Only `pyarrow` is installed initially. Install pandas into the same project
environment if its API is preferred:

```bash
PIP_CACHE_DIR="$PWD/.cache/pip" .venv/bin/python -m pip install pandas
```

PyArrow can read the files directly without pandas.

Verified table metadata is recorded in `metadata/TABLES.md`.

## Integrity check

```bash
shasum -a 256 -c metadata/SHA256SUMS
```

ADHD reference files have their own manifest:

```bash
shasum -a 256 -c metadata/adhd/SHA256SUMS
```

## Rebuild the ADHD mapping outputs

```bash
source .venv/bin/activate
./scripts/download_adhd_reference_data.sh
python scripts/build_adhd_gene_map.py
python scripts/build_malecns_dopamine_targets.py
python scripts/build_dopamine_downstream.py
```

The first script creates the human-gene to fly-ortholog and adult nervous-system
expression tables. The second creates a direct MaleCNS `bodyId` target list for
the dopamine axis. The two evidence layers are kept separate because Fly Cell
Atlas clusters are not measurements from individual MaleCNS neurons.
