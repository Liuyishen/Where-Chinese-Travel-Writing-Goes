# Interactive research website

This directory contains the bilingual interactive front end for **Where Chinese-Language Travel Writing Goes: Place, Mobility, and Cultural Imagination, 1980–2025**.

## What the current version contains

- An English-first research archive with a Chinese toggle and a coherent reading
  path from research questions to findings, method, limits, and public data.
- Signed RQ1 findings on place recurrence and author-concentration sensitivity;
  signed RQ2 findings on relation state, mobility, theme, and narrative
  function; and signed RQ3 findings on country coverage, concentration, and
  confirmed publication carriers.
- An interactive public-geometry map with a full-text **text × place relation**
  layer, a separate canonical **place-entity inventory**, and a separately
  styled bibliographic place-signal layer.
- Evidence cards and stated denominators throughout. The map only includes
  relationships with publishable geometry; archive-level findings can therefore
  have a larger denominator than the visual map.
- Direct links to versioned public data, method notes, scripts, and the release
  history in the repository.

## Important boundary

The website is a research interface, not a repository of copyrighted travel writing. It must only publish metadata, short lawful quotations, and material for which reuse is permitted. The displayed cases are a first interface dataset and are not a finished longitudinal sample.

## Data refresh

Run `npm run data:map` from this directory before `npm run build` after changing
the Q1 relation workbook or the corrected geocoding release. The command writes
only public metadata and geometry to `public/data/`:

- `q1_fulltext_text_place_relations.geojson`
- `q1_fulltext_entities.geojson`
- `q1_metadata_place_signals.geojson`
- `q1_map_release_summary.json`

The relation layer deliberately does **not** reconstruct a route from unrelated
point relations. Lines and polygons retain the geometry of the named place.

## Development

Install the declared dependencies, then run `npm run dev`. Build with `npm run build`.

The public release is deployed through the repository's GitHub Pages workflow.
The client uses relative data URLs so its map data also resolves under the Pages
project subpath.
