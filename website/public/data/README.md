# Q1 public map layers

This directory contains public metadata and geometry only. It contains no full
text, no bulk quotation, and no unlicensed reproduction.

| File | Unit | Permitted interpretation |
|---|---|---|
| `q1_fulltext_text_place_relations.geojson` | one canonical text × place relation | a text-supported relation to a named place; not necessarily a complete journey or reconstructed route |
| `q1_fulltext_entities.geojson` | one publishable canonical place entity | geographic reference inventory; not proof of authorial arrival |
| `q1_metadata_place_signals.geojson` | one metadata record × place signal | retrieval and bibliographic-visibility signal; never authorial-travel evidence |
| `q1_map_release_summary.json` | release-level counts and selection rules | provenance and audit summary |

`visited`, `mentioned`, `imagined_or_compared`, and `uncertain` must never be
collapsed into a single travel-footprint category. The exporter excludes
relationships that are semantically paused and any relation whose named place
does not yet have a publication-safe geometry.
