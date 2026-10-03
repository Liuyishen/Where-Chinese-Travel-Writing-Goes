# RQ1: place visibility — public research snapshot

## Question

Which places recur in Chinese-language travel writing, and which absences are visible in the current archive?

## Current evidence

The public release distinguishes two non-interchangeable layers.

| Layer | Unit | Current size | It can support |
|---|---|---:|---|
| Manually coded text–place layer | One canonically deduplicated verified text × one normalized place × one narrative relation | 107 texts; 410 relations; 372 entities | Descriptive patterns of arrival, mention, comparison, and uncertainty in the coded sample |
| Bibliographic-signal layer | One bibliography record × one raw place cue | 1,000 records; 1,091 signals; 603 specific-place or route signals | Preservation, retrieval, and sampling visibility across the wider source pool |

The layers are released as separate CSV files and must not be added together. A bibliographic cue is always `uncertain`/`metadata_only`; it does not show that its author visited the named place.

The 603 specific bibliographic signals have been rule-split into 1,633 atomic components. This is a retrieval and audit aid: it separates composite cues into reviewable components, but does not by itself normalize them into geographic entities or make them eligible for the full-text map.

## What is currently comparable

The full-text layer has an initial descriptive floor of 20 coded texts in each decade from the 1980s through the 2010s, and 25 in the 2020s. The associated CSV reports the denominator and relation-state counts for each decade. It is a deliberately constructed research sample, not a random sample of all Chinese travel writing published from 1980 to 2025.

The repeated-place table retains only entities occurring in two or more texts. It reports both text and author counts so that a recurrence created by one prolific writer is not mistaken for cross-author visibility.

## Map boundary

`rq1_candidate_map_points.csv` provides 68 point-geometry candidates whose normalized name, country/region, and point-type classification are compatible with an existing OpenStreetMap candidate. They are suitable for a clearly labelled candidate layer, not a definitive map: routes, rivers, mountains, countries, and regions remain line or polygon entities, and no centre point is invented for them. Every coordinate remains subject to human spatial review.

## Interpretation boundary

These materials support a first, evidence-led account of the current archive's geography of attention. They do not support a claim that unrepresented places were never written about, nor a definitive four-decade population trend. Missing material can result from publication, digitisation, cataloguing, access, and verification gaps as well as cultural attention.

## Reproduction

From the private research workbooks, run:

```bash
python3 scripts/build_rq1_public_release.py \
  --fulltext /path/to/RQ1_Q1规范去重_来源订正_2000补样_关系复核_空间签署_20261003.xlsx \
  --metadata /path/to/大池子_metadata_places与RQ1双层分析_20260929.xlsx \
  --places /path/to/RQ1_Q1规范去重_来源订正_2000补样_关系复核_空间签署_20261003.xlsx \
  --atomics /path/to/大池子_原子地点RQ1与全文追索队列_20260929.xlsx \
  --output-dir data/public
python3 scripts/validate_public_release.py
```

Review the result before publishing. The private workbooks are intentionally excluded from this repository.
