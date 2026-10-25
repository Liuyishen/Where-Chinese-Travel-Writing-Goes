# Public data release

This directory contains disclosure-safe aggregates from the current RQ1 place-visibility and signed RQ2 work. They are generated with the corresponding public-release scripts and contain no full texts, quotations, evidence locations, source URLs, or author/title-level rows.

The 2026-10-03 release includes canonical text-level deduplication and corrected source years. It reports 105 canonical texts, 400 canonical text–place relations, and 364 normalized entities. The raw historical identifiers remain private audit material and are not published here.

- `rq1_fulltext_by_decade.csv`: counts for the manually coded text–place layer.
- `rq1_repeated_places.csv`: normalized places occurring in at least two texts, without the underlying text rows.
- `rq1_candidate_map_points.csv`: 83 project-lead-confirmed point coordinates. They remain a point-only layer and do not replace line or polygon geometry for routes, rivers, mountains, countries, or regions.
- `rq1_author_concentration_sensitivity.csv`: signed Q1 recurrence and author-concentration metrics, including the leave-one-author-out lower bound.
- `rq1_leave_one_author_out.csv`: one aggregate sensitivity result per author; it contains no titles, URLs, excerpts, or relation-level evidence.
- `rq1_author_concentration_summary.json`: machine-readable summary for the signed author-concentration check.
- `rq2_mobility_baseline_metrics.csv`: signed relation-state and mobility-mode aggregates; it does not count trips.
- `rq2_mobility_by_era.csv`: relation-state and mobility-mode profiles by archive era; it is not a population trend series.
- `rq2_narrative_sequence_coverage.csv`: aggregate coverage of coded route-order fields and conservative adjacent narrative transitions.
- `rq2_mobility_summary.json`: machine-readable Q2 baseline totals and interpretation boundary.
- `rq2_theme_narration_summary.csv`: signed text-level theme and primary narrative-function counts, plus their non-exclusive retained-relation support.
- `rq2_theme_by_era.csv`: theme counts by archive era; it is an archive profile, not a population trend series.
- `rq2_theme_mobility_matrix.csv`: retained-relation mobility support for each signed text-level theme; themes intentionally overlap.
- `rq2_theme_place_state_matrix.csv`: retained-relation place-state support for each signed text-level theme; themes intentionally overlap.
- `rq2_theme_narration_summary.json`: machine-readable summary and interpretation boundary for the signed Q2 theme/narration layer.
- `rq1_bibliographic_signals_by_decade.csv`: separate counts for the larger bibliographic-signal layer.
- `rq1_bibliographic_atomic_components.csv`: rule-based splitting totals for the 603 specific bibliographic signals; these are not normalized entities.
- `rq1_release_summary.json`: release-wide totals and usage boundaries.

`corpus_metadata_public.csv` may be added later only after generating it from a private workbook and completing the review steps in `PUBLISH_MANIFEST.md`.

The public files are metadata-only and aggregate-only. They must not contain full text, scans, long quotations, session-bound URLs, access credentials, or text-level evidence locations.
