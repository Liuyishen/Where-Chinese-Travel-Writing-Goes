# Interactive research website

This directory contains the bilingual interactive front end for **Where Chinese-Language Travel Writing Goes: Place, Mobility, and Cultural Imagination, 1980–2025**.

## What the current version contains

- An English-first interface with a Chinese toggle.
- A full-text **text × place relation** layer. It currently publishes only rows
  that have a use-permitted full text, an AI semantic keep decision, and a
  publishable geometry for the named place.
- A separate canonical **place-entity inventory** layer.
- A toggleable, separately styled **bibliographic place-signal** layer. It is
  never represented as authorial arrival or route evidence.
- Filters for decade, relation type, place type, country/region text, and (for
  bibliographic signals) evidence grade.
- Evidence cards that retain the relation category, source record, and the
  boundary of each layer.

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

For production, connect this directory to a JavaScript-capable host such as Cloudflare Pages or Vercel. GitHub Pages alone is not the intended target for the current framework.
