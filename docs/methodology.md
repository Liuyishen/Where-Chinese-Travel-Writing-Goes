# Methodology

## Scope

The corpus covers Chinese-original travel writing published in mainland China between 1980 and 2025. Eligible records are independently readable pieces or chapters traceable to an author, carrier, and real place, with evidence of arrival, movement, stay, or on-site observation.

Guides, rankings, advertorials, unsourced reposts, translations, pure historical descriptions, and duplicate versions are excluded from formal analytical counts.

## Three layers

| Layer | Unit | Permitted use |
|---|---|---|
| Bibliographic / metadata pool | Chapter or independent piece | Sampling frame, metadata description, candidate mapping |
| Lawfully analyzable full-text subset | Verified complete text | Text analysis under documented access conditions |
| Close-reading cases | Selected piece | Interpretive reading with page-level evidence |

## Identifier model

- `REC-ID`: one record-level published piece or serial installment.
- `TXT-ID`: one textual entity; multiple editions or serial installments can relate to it.
- `SRC-ID`: one parent source or carrier.
- `PEV-ID`: one place-evidence relation, linked to a `TXT-ID`.

## Place evidence

Each mappable relation stores a normalized place name, place level, evidence URL or page, place state, and travel subject. `visited`, `mentioned`, `imagined_or_compared`, and `uncertain` are not interchangeable.

Routes and regions may use a representative point only for provisional visualization. They are not a substitute for line or polygon geometry.

## Access and rights

`metadata_only` means the record can support bibliographic description. `quote_only` permits only bounded quotation under applicable rules. `analysis_permitted` requires separately documented permission or an appropriate lawful basis. A page being publicly accessible does not by itself change the rights status.

## Deduplication

Exact author-title matching is followed by title similarity and version review. A similarity result is a review cue, not proof of a duplicate. First publication, reprints, excerpts, and collected editions are retained as explicit version relations.
