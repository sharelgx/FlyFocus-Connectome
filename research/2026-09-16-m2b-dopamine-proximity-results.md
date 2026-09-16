# M2B: curated candidate-cell-type dopamine proximity

Date: 2026-09-16
Status: exploratory circuit screen complete; functional validation remains open

## Question

Do explicitly bridgeable cell types highlighted by the M2A candidate-gene
expression screen have unusually strong direct connectivity with consensus
dopamine neurons in MaleCNS v1.0?

## Evidence chain and boundary

M2B keeps the following evidence layers separate:

```text
human ADHD evidence
  -> top Drosophila ortholog
  -> Fly Cell Atlas expression in a named cell type
  -> explicit name/annotation bridge to a MaleCNS neuron group
  -> MaleCNS connection-weight test against matched neurons
```

The chain generates circuit hypotheses. It does not show that the linked gene
was measured in each MaleCNS body ID, and it does not establish ADHD causality.

## Inputs and scope

- 211,577 annotated MaleCNS bodies;
- 396 neurons with `consensus_nt=dopamine`;
- all 151,856,684 rows in the 1.1 GB connection-weight graph;
- 11 candidate-linked cell-type bridges and two mushroom-body calibration
  groups;
- no synapse-coordinate or synapse-partner download.

Only explicit annotation rules were accepted. For example, Dm4 requires the
exact `Dm4` type and excludes the unrelated uppercase `DM4` olfactory
glomerular types. Unresolved detailed cell types remain unmapped.

## Statistical method

For each cell-type bridge, two directed hypotheses are tested:

1. consensus dopamine neurons to the candidate-linked group;
2. the candidate-linked group to consensus dopamine neurons.

The neuron-level response is the fraction of total incoming or outgoing
connection weight contributed by the relevant dopamine direction. The null
distribution uses 10,000 stratified bootstrap samples matched on:

- anatomical family;
- total connection-strength quintile;
- connection-degree quintile.

Only the current test group and dopamine neurons are excluded from its random
background. Benjamini-Hochberg correction covers all 22 candidate tests.

## Significant exploratory results

### `FoxP` / LC10c: elevated dopamine input

- human genes: `FOXP1 / FOXP2`;
- fly ortholog: `FoxP`;
- Fly Cell Atlas cell type: lobula columnar neuron LC10c;
- MaleCNS LC10c neurons tested: 255;
- neurons with a direct consensus-dopamine input: 195;
- direct dopamine-to-LC10c edges: 328;
- total direct dopamine-to-LC10c weight: 443;
- mean dopamine input fraction: 0.002625;
- matched-null mean: 0.001047;
- fold versus matched null: 2.51;
- empirical p: 0.000100;
- BH FDR across 22 candidate tests: 0.00110.

The M2A expression source contains one adult optic-lobe LC10c row for `FoxP`,
with spread 0.9333. This is a strong hypothesis-generating bridge, but one
source row is not independent replication.

### `Lar` / TmY4: elevated output to dopamine neurons

- human gene: `PTPRF`;
- fly ortholog: `Lar`;
- Fly Cell Atlas cell type: transmedullary Y neuron TmY4;
- MaleCNS TmY4 neurons tested: 562;
- neurons with a direct output to consensus dopamine neurons: 333;
- direct TmY4-to-dopamine edges: 430;
- total direct TmY4-to-dopamine weight: 788;
- mean dopamine-directed output fraction: 0.001571;
- matched-null mean: 0.000229;
- fold versus matched null: 6.87;
- empirical p: 0.000100;
- BH FDR across 22 candidate tests: 0.00110.

The M2A expression source contains five supporting TmY4 rows for `Lar`, with a
maximum spread of 1.0. Several records derive from female or sex-unspecified
adult material, while MaleCNS is male; sex transfer must therefore be tested,
not assumed.

## Negative results retained

The other nine candidate-linked bridges did not pass FDR < 0.05 in either
direction. In particular, Dm1, Dm4, Lawf2, photoreceptors, Hugin-RG, ITP, and
CRZ had zero direct consensus-dopamine weight in this graph under the accepted
rules. ALPN and the octopamine group had direct connections but were not
enriched relative to matched neurons after correction.

These null results are part of the experiment and are not replaced with an
uncorrected network visualization.

## Calibration

The known mushroom-body comparators behaved as expected:

- Kenyon cells: dopamine input fraction 21.18-fold above matched null;
- MBONs: dopamine input fraction 4.82-fold above matched null.

Both calibration tests reached the minimum Monte Carlo p-value of 0.000100.
They are reported as method checks and were not included in the 22 candidate
FDR tests.

## Validation

- A second complete run produced identical hashes for every M2B CSV/JSON
  output.
- An independent Arrow filtering calculation recovered exactly 328 edges and
  weight 443 for dopamine to LC10c, and 430 edges and weight 788 for TmY4 to
  dopamine.
- Python compilation and CSV format checks pass.

## Interpretation

M2B identifies two testable circuit hypotheses:

1. `FoxP` perturbation in LC10c may alter dopamine-modulated visual feature
   selection or attention-like behavior.
2. `Lar` perturbation in TmY4 may alter a visual pathway that provides direct
   input to dopamine neurons.

LC10 neurons are established visual projection neurons associated with
feature-driven behavior, and TmY4 is an adult visual-system transmedullary Y
cell type. That context supports testing these hypotheses but does not prove
that either circuit is an ADHD homolog.

## Next experimental gate

The strongest next step is a two-gene, two-cell-type wet-lab design:

- `FoxP` knockdown or rescue restricted to LC10c;
- `Lar` knockdown or rescue restricted to TmY4;
- locomotor, sleep, visual competition/cueing, and appropriate sensory/motor
  control assays;
- independent driver lines, genetic background controls, and blinded analysis;
- male and female cohorts analyzed separately.

Before wet work, the computational robustness gate should repeat M2B across
reasonable neurotransmitter and minimum-edge thresholds and, where possible,
confirm the cell-type bridges in an independent adult-brain expression source.

## Reproducible artifacts

- `scripts/run_m2b_dopamine_proximity.py`
- `outputs/m2b-cell-type-bridges.csv`
- `outputs/m2b-dopamine-proximity.csv`
- `outputs/m2b-summary.json`

## Context sources

- MaleCNS data tables: <https://male-cns.janelia.org/download/>
- LC visual projection neurons and feature-driven behavior:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC5293491/>
- TmY4 ontology and MaleCNS-linked examples:
  <https://mayo.inf.ed.ac.uk/blog/2022/01/01/tmy4-fbbt_00003821/>
- dopamine and visual cueing in flies:
  <https://pubmed.ncbi.nlm.nih.gov/27571359/>
