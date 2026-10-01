#!/usr/bin/env python3
"""Export disclosure-safe RQ1 aggregates from private research workbooks.

This script publishes only counts, normalized entity names and entity-level
metrics. It deliberately omits full text, quotations, evidence locations,
source URLs, titles and author names.
"""
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import load_workbook


def rows(sheet):
    iterator = sheet.iter_rows(values_only=True)
    headers = next(iterator)
    for values in iterator:
        if any(value not in (None, "") for value in values):
            yield dict(zip(headers, values))


def write_csv(path, fieldnames, records):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fulltext", required=True, type=Path)
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    fulltext_book = load_workbook(args.fulltext, read_only=True, data_only=True)
    relation_rows = list(rows(fulltext_book["正文关系_396"]))
    entity_rows = list(rows(fulltext_book["实体主表_357"]))

    by_era = defaultdict(lambda: {"text_ids": set(), "relations": 0, "states": Counter()})
    for row in relation_rows:
        era = row["年代"] or "未定"
        bucket = by_era[era]
        bucket["text_ids"].add(row["text_id"])
        bucket["relations"] += 1
        bucket["states"][row["地点状态"]] += 1

    era_order = ["1980s", "1990s", "2000s", "2010s", "2020s", "未定"]
    fulltext_eras = []
    for era in era_order:
        bucket = by_era.get(era)
        if not bucket:
            continue
        fulltext_eras.append({
            "decade": era,
            "text_count": len(bucket["text_ids"]),
            "text_place_relations": bucket["relations"],
            "visited": bucket["states"]["visited"],
            "mentioned": bucket["states"]["mentioned"],
            "imagined_or_compared": bucket["states"]["imagined_or_compared"],
            "uncertain": bucket["states"]["uncertain"],
        })
    write_csv(
        args.output_dir / "rq1_fulltext_by_decade.csv",
        list(fulltext_eras[0].keys()),
        fulltext_eras,
    )

    repeated = []
    for row in entity_rows:
        if (row["关联文本数"] or 0) >= 2:
            repeated.append({
                "place_id": row["merged_place_id"],
                "normalized_place": row["规范地点名"],
                "country_or_region": row["国家地区"],
                "text_count": row["关联文本数"],
                "author_count": row["独立作者数"],
                "visited_text_count": row["visited文本数"],
            })
    repeated.sort(key=lambda row: (-row["text_count"], -row["author_count"], row["normalized_place"] or ""))
    write_csv(
        args.output_dir / "rq1_repeated_places.csv",
        ["place_id", "normalized_place", "country_or_region", "text_count", "author_count", "visited_text_count"],
        repeated,
    )

    metadata_book = load_workbook(args.metadata, read_only=True, data_only=True)
    metadata_era_rows = list(rows(metadata_book["年代证据结构"]))
    metadata_eras = [{
        "decade": row["年代"],
        "metadata_place_signals": row["地点信号行数"],
        "distinct_records": row["涉及独立记录数"],
        "specific_place_or_route_signals": row["其中具体地点或路线"],
        "regional_signals": row["其中区域覆盖线索"],
        "retrieval_only_signals": row["仅追索线索"],
    } for row in metadata_era_rows]
    write_csv(
        args.output_dir / "rq1_bibliographic_signals_by_decade.csv",
        list(metadata_eras[0].keys()),
        metadata_eras,
    )

    summary = {
        "release_date": "2026-10-01",
        "fulltext_layer": {
            "verified_texts": len({row["text_id"] for row in relation_rows}),
            "text_place_relations": len(relation_rows),
            "normalized_place_entities": len(entity_rows),
            "repeated_place_entities": len(repeated),
            "rights_boundary": "Counts derive from manually coded, quote_only research records; no full texts are released.",
        },
        "bibliographic_layer": {
            "metadata_place_signals": sum(row["metadata_place_signals"] for row in metadata_eras),
            "specific_place_or_route_signals": sum(row["specific_place_or_route_signals"] for row in metadata_eras),
            "rights_boundary": "Bibliographic signals are metadata_only and uncertain. They are not author-visit points and are never combined with full-text relation counts.",
        },
    }
    with (args.output_dir / "rq1_release_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
