#!/usr/bin/env python3
"""Build disclosure-safe Q1 author-concentration diagnostics and figures."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from openpyxl import load_workbook


def sheet_rows(workbook, sheet_name):
    sheet = workbook[sheet_name]
    iterator = sheet.iter_rows(values_only=True)
    headers = next(iterator)
    return [dict(zip(headers, row)) for row in iterator if any(value not in (None, "") for value in row)]


def place_metrics(relations):
    places = defaultdict(lambda: {"texts": set(), "authors": set(), "relations": 0})
    labels = {}
    for relation in relations:
        place_id = relation["merged_place_id"]
        metric = places[place_id]
        metric["texts"].add(relation["canonical_text_id"])
        metric["authors"].add(relation["作者"])
        metric["relations"] += 1
        labels[place_id] = relation["规范地点名"]
    return places, labels


def repeated_count(relations):
    places, _ = place_metrics(relations)
    return sum(len(metric["texts"]) >= 2 for metric in places.values())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--figure-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.figure_dir.mkdir(parents=True, exist_ok=True)

    workbook = load_workbook(args.workbook, read_only=True, data_only=True)
    relations = sheet_rows(workbook, "规范关系_410")
    reviews = {
        row["canonical_relationship_id"]: row
        for row in sheet_rows(workbook, "关系AI复核与人工签署_20261006")
    }
    if set(relation["canonical_relationship_id"] for relation in relations) != set(reviews):
        raise ValueError("Every canonical relation must have a sign-off row.")

    decisions = Counter(reviews[relation["canonical_relationship_id"]]["人工签署决定"] for relation in relations)
    if set(decisions) != {"保留", "暂停"}:
        raise ValueError(f"Unexpected sign-off decisions: {dict(decisions)}")
    retained = [relation for relation in relations if reviews[relation["canonical_relationship_id"]]["人工签署决定"] == "保留"]
    places, labels = place_metrics(retained)
    recurrence = Counter(len(metric["texts"]) for metric in places.values())
    repeated = {place_id: metric for place_id, metric in places.items() if len(metric["texts"]) >= 2}
    cross_author = {place_id: metric for place_id, metric in repeated.items() if len(metric["authors"]) >= 2}
    single_author = {place_id: metric for place_id, metric in repeated.items() if len(metric["authors"]) == 1}
    author_counts = Counter(relation["作者"] for relation in retained)

    leave_one_out = []
    for author, count in author_counts.items():
        without_author = [relation for relation in retained if relation["作者"] != author]
        remaining_places, _ = place_metrics(without_author)
        leave_one_out.append({
            "author": author,
            "relationships_removed": count,
            "repeated_places_remaining": repeated_count(without_author),
            "cross_author_repeated_places_remaining": sum(
                len(metric["texts"]) >= 2 and len(metric["authors"]) >= 2
                for metric in remaining_places.values()
            ),
        })
    leave_one_out.sort(key=lambda row: (row["repeated_places_remaining"], row["author"]))

    hhi = sum((count / len(retained)) ** 2 for count in author_counts.values())
    top_ten_share = sum(count for _, count in author_counts.most_common(10)) / len(retained)
    audit_rows = [
        {
            "metric": "signed_relation_universe",
            "value": len(relations),
            "definition": "All canonical text-place relationships with a recorded project-lead decision.",
        },
        {
            "metric": "retained_relations",
            "value": len(retained),
            "definition": "Relationships signed 保留 and used for the current Q1 analysis.",
        },
        {
            "metric": "paused_relations",
            "value": decisions["暂停"],
            "definition": "Relationships signed 暂停 and excluded from the current Q1 analysis.",
        },
        {
            "metric": "normalized_places_in_retained_layer",
            "value": len(places),
            "definition": "Distinct normalized entities represented by retained relations.",
        },
        {
            "metric": "repeated_places_in_retained_layer",
            "value": len(repeated),
            "definition": "Entities occurring in two or more distinct texts after signed pauses are excluded.",
        },
        {
            "metric": "cross_author_repeated_places",
            "value": len(cross_author),
            "definition": "Repeated entities associated with two or more distinct authors.",
        },
        {
            "metric": "single_author_repeated_places",
            "value": len(single_author),
            "definition": "Repeated entities whose current recurrence is generated by one author only.",
        },
        {
            "metric": "leave_one_author_out_min_repeated_places",
            "value": min(row["repeated_places_remaining"] for row in leave_one_out),
            "definition": "Smallest repeated-place count after removing every relation by any one author in turn.",
        },
        {
            "metric": "top_ten_author_relation_share",
            "value": round(top_ten_share, 6),
            "definition": "Share of retained relation rows associated with the ten highest-volume authors; use author-aware entity metrics rather than raw row counts for visibility claims.",
        },
        {
            "metric": "author_relation_hhi",
            "value": round(hhi, 6),
            "definition": "Herfindahl-Hirschman Index over retained relation rows by author.",
        },
    ]
    with (args.output_dir / "rq1_author_concentration_sensitivity.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value", "definition"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(audit_rows)

    with (args.output_dir / "rq1_leave_one_author_out.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["author", "relationships_removed", "repeated_places_remaining", "cross_author_repeated_places_remaining"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(leave_one_out)

    figure_counts = sorted(recurrence.items())
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    figure, axis = plt.subplots(figsize=(7.4, 4.5))
    bars = axis.bar([str(count) for count, _ in figure_counts], [entity_count for _, entity_count in figure_counts], color="#5B4B8A", width=0.62)
    axis.set_title("Place recurrence in the signed Q1 archive", loc="left", weight="bold")
    axis.set_xlabel("Distinct texts in which a normalized place appears")
    axis.set_ylabel("Normalized places")
    axis.set_ylim(0, max(entity_count for _, entity_count in figure_counts) * 1.12)
    for bar, (_, entity_count) in zip(bars, figure_counts):
        axis.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, str(entity_count), ha="center", va="bottom")
    axis.text(0.98, 0.95, "479 retained relations · 433 normalized places", transform=axis.transAxes, va="top", ha="right", color="#4E4A52")
    axis.spines[["top", "right"]].set_visible(False)
    figure.tight_layout()
    figure.savefig(args.figure_dir / "q1_place_recurrence_distribution_20261025.svg", format="svg")
    figure.savefig(args.figure_dir / "q1_place_recurrence_distribution_20261025.png", dpi=240)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(7.4, 4.8))
    combinations = Counter((len(metric["texts"]), len(metric["authors"])) for metric in repeated.values())
    for (text_count, author_count), entity_count in sorted(combinations.items()):
        color = "#B14A3B" if author_count == 1 else "#2D6C91"
        axis.scatter(text_count, author_count, color=color, s=80 + entity_count * 20, alpha=0.9, edgecolor="white", linewidth=0.8)
        axis.annotate(f"n={entity_count}", (text_count, author_count), xytext=(7, 7), textcoords="offset points", fontsize=9, weight="bold")
    axis.plot([1, 4], [1, 4], color="#999999", linewidth=1, linestyle="--", zorder=0)
    axis.set_xlim(1.75, 4.25)
    axis.set_ylim(0.75, 4.5)
    axis.set_xticks([2, 3, 4])
    axis.set_yticks([1, 2, 3, 4])
    axis.set_title("Repeated places: texts versus independent authors", loc="left", weight="bold")
    axis.set_xlabel("Distinct texts")
    axis.set_ylabel("Distinct authors")
    axis.text(0.02, 0.95, "Bubble size = normalized places · Blue: cross-author · Red: single-author", transform=axis.transAxes, va="top", color="#4E4A52")
    axis.spines[["top", "right"]].set_visible(False)
    figure.tight_layout(rect=[0, 0, 1, 0.94])
    figure.savefig(args.figure_dir / "q1_repeated_places_author_concentration_20261025.svg", format="svg")
    figure.savefig(args.figure_dir / "q1_repeated_places_author_concentration_20261025.png", dpi=240)
    plt.close(figure)

    summary = {
        "release_date": "2026-10-25",
        "signed_relation_universe": len(relations),
        "retained_relations": len(retained),
        "paused_relations": decisions["暂停"],
        "normalized_places": len(places),
        "recurrence_histogram": {str(key): value for key, value in sorted(recurrence.items())},
        "repeated_places": len(repeated),
        "cross_author_repeated_places": len(cross_author),
        "single_author_repeated_places": len(single_author),
        "leave_one_author_out_repeated_place_range": [
            min(row["repeated_places_remaining"] for row in leave_one_out),
            max(row["repeated_places_remaining"] for row in leave_one_out),
        ],
        "top_ten_author_relation_share": round(top_ten_share, 6),
        "author_relation_hhi": round(hhi, 6),
    }
    (args.output_dir / "rq1_author_concentration_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
