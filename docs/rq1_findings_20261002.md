# RQ1 findings: the current archive's geography of attention

## Claim and evidence boundary

This is a conclusion about the current, verified research archive—not a census of all Chinese-language travel writing published between 1980 and 2025. The manually coded layer contains 106 texts, 396 text–place relations, and 357 conservatively normalized place entities. Every text has a recovered source URL; the accessible text records remain `quote_only`, not `analysis_permitted`.

The evidence is deliberately separated from the larger bibliographic layer of 1,000 records and 1,091 place signals. Its 603 specific-place or route signals have been rule-split into 1,633 audit components, but those components remain `metadata_only` and `uncertain`. They cannot be counted as author arrivals or merged with the 396 coded relations.

## Finding 1: recurrence is limited and structurally uneven

Only 30 of the 357 normalized entities occur in two or more texts. The remaining 327 occur in one text each. Of the 30 repeated entities, 26 recur across two or more authors and four are repeated only within one author's work. The latter remain valuable evidence of a writer's itinerary or long-term attention, but they are not evidence of general cultural visibility.

The most frequent cross-author entities in the current archive are Kunming (four texts, four authors), Tokyo (three texts, three authors), and New Delhi (three texts, three authors). Other cross-author recurrences occur only twice each. The result is not a stable league table of destinations; it is a pattern of sparse recurrence alongside many singular, specific encounters.

## Finding 2: most coded relations are arrival or observation, but not all are footprints

Of the 396 relations, 324 are `visited`, 61 are `mentioned`, nine are `imagined_or_compared`, and two remain `uncertain`. A point layer must therefore not conflate a literary comparison, background reference, or historical association with physical arrival. The archive's geography is at once a geography of movement and a geography of cultural reference.

## Finding 3: the current sample's decade profiles differ, but only descriptively

The coded relation counts are 118 in the 1980s, 63 in the 1990s, 63 in the 2000s, 62 in the 2010s, and 89 in the 2020s. The corpus has 20 texts in each of the first four decade groups and 25 in the 2020s, providing an initial descriptive floor rather than a probability sample. These figures can identify archive patterns worth explaining, but cannot establish a population-level historical trend.

## Finding 4: absence is an evidence category, not an empty space

The defensible statement is that a place is absent from the current verified text–place layer, or appears only as a bibliographic signal without verified full-text evidence. It is not defensible to say that Chinese travel writing has historically ignored that place. Missingness can arise from digitisation, catalogue structure, source access, rights constraints, and incomplete verification as well as from literary attention.

## Map implementation

The project supplies 68 OSM-matched point candidates as a separately labelled candidate layer. They are not a replacement for complete spatial geometry: countries, regions, rivers, mountains, and routes remain polygon or line entities, and no fabricated centre point is supplied. The map must visibly distinguish this candidate layer from verified text–place relations and bibliographic `related` signals.

## Audit status

All 30 repeated entities and both `uncertain` relations were selected for AI structural audit: 69 relations across 42 texts. Twenty-six texts passed automated re-visitation of a readable page with matching title and author strings. Sixteen require human return-to-page checking because of 403 responses, dynamic rendering, or byline presentation; no location state or rights status was silently changed.
