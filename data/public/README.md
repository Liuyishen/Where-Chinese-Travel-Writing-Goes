# Public data release

This directory contains disclosure-safe aggregates from the current RQ1 place-visibility work. They are generated with `scripts/build_rq1_public_release.py` and contain no full texts, quotations, evidence locations, source URLs, or author/title-level rows.

The 2026-10-03 release includes canonical text-level deduplication and corrected source years. It reports 105 canonical texts, 400 canonical text–place relations, and 364 normalized entities. The raw historical identifiers remain private audit material and are not published here.

- `rq1_fulltext_by_decade.csv`: counts for the manually coded text–place layer.
- `rq1_repeated_places.csv`: normalized places occurring in at least two texts, without the underlying text rows.
- `rq1_candidate_map_points.csv`: 68 OSM-matched point candidates, explicitly marked as awaiting human spatial review.
- `rq1_bibliographic_signals_by_decade.csv`: separate counts for the larger bibliographic-signal layer.
- `rq1_bibliographic_atomic_components.csv`: rule-based splitting totals for the 603 specific bibliographic signals; these are not normalized entities.
- `rq1_release_summary.json`: release-wide totals and usage boundaries.

`corpus_metadata_public.csv` may be added later only after generating it from a private workbook and completing the review steps in `PUBLISH_MANIFEST.md`.

The public files are metadata-only and aggregate-only. They must not contain full text, scans, long quotations, session-bound URLs, access credentials, or text-level evidence locations.
