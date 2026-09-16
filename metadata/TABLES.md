# Verified Feather tables

Verified locally with PyArrow 25.0.1 on 2026-09-15.

| File | Bytes | Rows | Columns | Record batches |
| --- | ---: | ---: | ---: | ---: |
| `body-annotations-male-cns-v1.0-minconf-0.5.feather` | 14,483,314 | 211,577 | 36 | 4 |
| `body-neurotransmitters-male-cns-v1.0.feather` | 43,282,834 | 1,835,518 | 10 | 29 |
| `connectome-weights-male-cns-v1.0-minconf-0.5.feather` | 1,051,241,946 | 151,856,684 | 3 | 2,318 |

The local byte sizes match the official Google Cloud Storage `Content-Length`
values. All files also pass the SHA-256 checks in `SHA256SUMS`.

## Fields

- Annotations (36): `assignedOlHex1`, `assignedOlHex2`, `bodyId`, `flywireType`,
  `group`, `instance`, `somaSide`, `statusLabel`, `superclass`, `type`, `vfbId`,
  `hemibrainType`, `itoleeHl`, `supertype`, `birthtime`, `mancBodyid`, `mancGroup`,
  `mancType`, `subclass`, `synonyms`, `class`, `rootSide`, `somaNeuromere`,
  `trumanHl`, `dimorphism`, `matchingNotes`, `entryNerve`, `mancSerial`,
  `mcnsSerial`, `serialMotif`, `fruDsx`, `exitNerve`, `receptorType`,
  `somaLocation`, `tosomaLocation`, `status`
- Neurotransmitters (10): `body`, `cell_type`, `total_nt_predictions`,
  `predicted_nt_confidence`, `predicted_nt`, `ground_truth`,
  `celltype_total_nt_predictions`, `celltype_predicted_nt`,
  `celltype_predicted_nt_confidence`, `consensus_nt`
- Connection weights (3): `body_pre`, `body_post`, `weight`
