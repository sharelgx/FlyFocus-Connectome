# M2A: neural-class enrichment and candidate prioritization

Date: 2026-09-16
Status: first computational experiment complete; circuit-level M2B remains open

## Question

Do the highest-DIOPT Drosophila orthologs of the human ADHD candidate set show
more expression in broad adult neural cell classes than similarly expressed
non-candidate fly genes?

## Inputs

- 79 highest-DIOPT human-fly mapping rows from M1, collapsing to 75 unique fly
  genes after shared orthologs are merged.
- FlyBase FB2026_02 Fly Cell Atlas slimmed expression for 17,372 genes and 22
  broad cell classes.
- The M1 adult nervous-system single-cell subset for descriptive, detailed
  cell-type highlights.

## Method

For each gene, the matching variable is its mean positive-cell percentage over
six broad neural classes: neuron, interneuron, motor neuron, sensory neuron,
sensory-organ cell, and glial cell. Candidate genes are matched to
non-candidate genes in 50 expression quantiles. Ten thousand deterministic
matched permutations (seed 20260916) estimate one-sided empirical p-values.
Benjamini-Hochberg correction is applied across the six tests.

The candidate priority score is a declared exploratory heuristic:

- human evidence: up to 35 points;
- DIOPT orthology: up to 25 points;
- broad neural expression: up to 20 points;
- neural versus non-neural specificity: up to 10 points;
- existing FlyBase disease models: up to 10 points.

It is not a probability, p-value, or causal score.

## Primary result

No broad neural class is significantly enriched at FDR < 0.05.

| Cell class | Candidate mean positive % | Matched null % | Difference, pp | Empirical p | BH FDR |
| --- | ---: | ---: | ---: | ---: | ---: |
| motor neuron | 19.853 | 19.099 | +0.754 | 0.196 | 0.945 |
| interneuron | 13.640 | 13.262 | +0.378 | 0.315 | 0.945 |
| neuron | 16.160 | 16.371 | -0.211 | 0.655 | 0.954 |
| glial cell | 15.493 | 15.708 | -0.215 | 0.602 | 0.954 |
| sensory neuron | 16.080 | 16.696 | -0.616 | 0.836 | 0.954 |
| sensory-organ cell | 15.093 | 16.027 | -0.934 | 0.954 | 0.954 |

This result does not show that the ADHD-derived ortholog set is absent from the
nervous system. It shows that, after matching overall neural expression, the
set is not unusually concentrated in any of these six coarse classes.

## Exploratory candidate ranking

The top new candidates under the declared heuristic are:

| Rank | Human | Fly | Score | Interpretation |
| ---: | --- | --- | ---: | --- |
| 1 | `PTPRF` | `Lar` | 93.02 | dual human evidence, strong orthology, broad neural expression, disease models |
| 2 | `FOXP1 / FOXP2` | `FoxP` | 78.02 | dual evidence and strong neural specificity |
| 3 | `CAMKV` | `CaMKI` | 68.63 | dual evidence and broad neural expression |
| 4 | `SEMA6D` | `Sema1a` | 68.22 | MAGMA evidence and neural specificity |
| 5 | `CYHR1` | `CG32486` | 67.90 | credible-set evidence and high DIOPT score |
| 6 | `DCC` | `fra` | 63.33 | dual evidence, high DIOPT score, one disease model |

`MEF2C / Mef2`, a literature control rather than a new discovery, ranks eighth.

## Detailed cell-type signals are descriptive

Examples from the candidate-only adult nervous-system subset include:

- `Lar`: lamina wide-field 2, TmY4, and adult octopaminergic neurons;
- `FoxP`: Dm4 medullary amacrine, LC10c lobula columnar, and lineage 16
  secondary neurons;
- `CaMKI`: photoreceptor, dorsal-margin photoreceptor, and ocellar retinula
  cells;
- `Sema1a`: Hugin, ITP, and antennal-lobe projection neurons;
- `CG32486`: corazonin neurons and Dm1/Dm4 medullary amacrine neurons.

These are maxima across source clusters and are hypothesis-generating. They do
not constitute enrichment tests, and they cannot be assigned directly to
MaleCNS body IDs.

## Interpretation and next gate

The absence of broad-class enrichment argues for a finer-grained hypothesis:
the relevant signal, if present, may be restricted to particular visual,
neuromodulatory, mushroom-body, central-complex, or sleep-related cell types.

M2B should therefore curate only evidence-supported FlyBase-to-MaleCNS type
bridges for the leading genes and test their proximity to dopamine-related
circuits against source-strength- and degree-matched random neurons. A null
M2B result must be retained rather than replaced by an uncorrected network
visualization.

## Reproducible artifacts

- `scripts/run_m2_neural_enrichment.py`
- `outputs/m2-neural-cell-class-enrichment.csv`
- `outputs/m2-candidate-priority.csv`
- `outputs/m2-candidate-cell-type-highlights.csv`
- `outputs/m2-summary.json`

## Scientific context

- MaleCNS data and graph tables: <https://male-cns.janelia.org/download/>
- dopamine and visual attention in the mushroom body:
  <https://pubmed.ncbi.nlm.nih.gov/27571359/>
- dopamine-mushroom-body saliency choice circuit:
  <https://pubmed.ncbi.nlm.nih.gov/17600217/>
- dopaminergic inputs and sleep control in the mushroom body:
  <https://pubmed.ncbi.nlm.nih.gov/26617493/>
