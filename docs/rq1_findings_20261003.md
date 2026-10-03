# RQ1 findings: the current archive's geography of attention

## Claim and evidence boundary

This is a conclusion about the current verified research archive, not a census of all Chinese-language travel writing published between 1980 and 2025. The public aggregate uses 105 canonically deduplicated texts, 400 text–place relations, and 364 conservatively normalized place entities. One confirmed historical duplicate—Tang Shizeng's chapter “死亡之路”—is counted once while its private audit trail is retained. Accessible material remains `quote_only` or, for a user-supplied partial text, `partial_text`; no full text is released or used for batch NLP.

The bibliographic layer remains separate: 1,000 records contain 1,091 place signals, including 603 specific-place or route signals. Those signals are `metadata_only` and `uncertain`; they are neither author-arrival claims nor additions to the 400 coded relations.

## Finding 1: recurrence is limited and structurally uneven

The current archive contains many singular, specific encounters. Repeated places should be read with both text count and author count: a repeated location within one writer's work can show an itinerary or sustained attention, but it is not by itself evidence of broad cultural visibility. Cross-author recurrence is the stronger Q1 indicator.

## Finding 2: arrival is not the only place relation

The 400 relations distinguish `visited`, `mentioned`, `imagined_or_compared`, and `uncertain`. A place in a comparison, institutional context, or historical aside is not silently turned into a footprint. The added partial annotation for “东京：日本初印象” demonstrates this rule: Tokyo, Narita, NHK and the embassy are coded as evidenced arrival/stay relations; Shanghai, Taipei and Europe remain comparison relations.

## Finding 3: decade counts are descriptive, not population trends

The canonical sample contains 21 texts in the 1980s, 21 in the 1990s, 18 in the 2000s, 20 in the 2010s, and 25 in the 2020s. Its relation counts are respectively 118, 69, 63, 62, and 88. These numbers describe the present verified archive after source correction and deduplication. They cannot prove a historical rise, decline, or absence without a more comparable sampling frame.

## Finding 4: absence is an evidence category

A place can be absent from the verified text layer but present in bibliographic retrieval signals, or absent because of digitisation, catalogue structure, access, rights, and verification gaps. Q1 can therefore identify what this archive makes visible; it cannot claim that Chinese travel writing historically ignored every absent place.

## Map implementation

The public release retains 68 OpenStreetMap-compatible point candidates as a clearly labelled, pending-human-review layer. New Tokyo-related point entities are not added to that layer until their geometry is manually verified. Rivers, mountains, routes, countries and regions remain line or polygon entities rather than invented centre points.

## Remaining audit work

The source correction, canonical-ID map, relationship back-links and public aggregate are now in place. Remaining work concerns wider comparable sampling, manual spatial sign-off for point candidates and non-point geometries, and human adjudication of access/page issues—not silent recoding of literary place states.
