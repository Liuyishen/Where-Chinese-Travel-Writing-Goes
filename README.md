# Where Chinese Travel Writing Goes

## Place, Mobility, and Cultural Imagination, 1980–2025

This repository documents a computational humanities project on Chinese-language travel writing published in mainland China. It asks which places become visible, how mobility is narrated, and how destinations and media change from 1980 to 2025.

The project is research infrastructure, not a collection of full texts. It separates bibliographic metadata, lawfully analyzable full texts, and close-reading cases. The record unit is a chapter or independently readable piece; a book is a parent source.

## Public contents

- A documented data model and controlled vocabularies.
- A disclosure-safe RQ1 place-visibility snapshot, with separate full-text and bibliographic-signal aggregates.
- Scripts for making a metadata-only public release from a private workbook.
- A reproducible workflow for identifiers, deduplication, and place evidence.
- Citation information and a release checklist.

## Excluded from this repository

- Copyrighted full texts, scans, long quotations, and access-controlled database exports.
- Cookies, passwords, institutional access links, and session data.
- Unverified source-level leads presented as analytical records.

`visited`, `mentioned`, `imagined_or_compared`, and `uncertain` are different place states. `metadata_only`, `quote_only`, and `analysis_permitted` are different access states. A public webpage is not automatically permission for full-text analysis.

## Reproducing a metadata release

Keep the working workbook outside the public tree (or in ignored `data/private/`), then run:

```bash
python3 scripts/build_public_metadata.py --input data/private/master.xlsx --output data/public/corpus_metadata_public.csv
python3 scripts/validate_public_release.py
```

Review the generated CSV before committing. See [`PUBLISH_MANIFEST.md`](PUBLISH_MANIFEST.md) and [`CITATION.cff`](CITATION.cff).

## Current RQ1 snapshot

The current public release records 106 manually coded texts, 396 text–place relations, and 357 normalized place entities. The larger bibliographic layer contains 1,091 place signals, including 603 specific-place or route signals. These are deliberately separate analytical layers: see [the RQ1 note](docs/rq1_place_visibility.md), [the current findings](docs/rq1_findings_20261002.md), and `data/public/`.
