#!/usr/bin/env python3
"""Build disclosure-safe signed Q2 mobility and narration baseline outputs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from openpyxl import load_workbook


ERAS = ["1980s", "1990s", "2000s", "2010s", "2020s"]
STATES = ["visited", "mentioned", "imagined_or_compared", "uncertain"]
MODE_ORDER = [
    "road", "walking", "air", "water", "rail", "fieldwork_or_reporting",
    "migration_or_residence", "border_crossing", "running", "unspecified",
]


def sheet_rows(workbook, sheet_name):
    sheet = workbook[sheet_name]
    iterator = sheet.iter_rows(values_only=True)
    headers = next(iterator)
    return [dict(zip(headers, row)) for row in iterator if any(value not in (None, "") for value in row)]


def write_csv(path, rows, headers):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sequence_metrics(relations):
    by_text = defaultdict(list)
    for relation in relations:
        try:
            order = int(str(relation["路线顺序"]).strip())
        except (TypeError, ValueError):
            continue
        by_text[relation["canonical_text_id"]].append((order, relation))

    texts_with_two_nodes = []
    ordered_relation_count = 0
    transition_count = 0
    for text_id, rows in by_text.items():
        distinct_orders = {order for order, _ in rows}
        ordered_relation_count += len(rows)
        if len(distinct_orders) >= 2:
            texts_with_two_nodes.append(text_id)
            transition_count += len(distinct_orders) - 1
    return {
        "texts_with_any_ordered_node": len(by_text),
        "ordered_relation_rows": ordered_relation_count,
        "texts_with_two_or_more_ordered_nodes": len(texts_with_two_nodes),
        "conservative_adjacent_narrative_transitions": transition_count,
    }


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
    reviews = {row["canonical_relationship_id"]: row for row in sheet_rows(workbook, "关系AI复核与人工签署_20261006")}
    relation_ids = {row["canonical_relationship_id"] for row in relations}
    if relation_ids != set(reviews):
        raise ValueError("Every canonical relation must have a sign-off row.")
    decisions = Counter(reviews[row["canonical_relationship_id"]]["人工签署决定"] for row in relations)
    if set(decisions) != {"保留", "暂停"}:
        raise ValueError(f"Unexpected sign-off decisions: {dict(decisions)}")
    retained = [row for row in relations if reviews[row["canonical_relationship_id"]]["人工签署决定"] == "保留"]

    state_counts = Counter(row["地点状态"] for row in retained)
    mode_counts = Counter((row["移动方式"] or "unspecified") for row in retained)
    visited = [row for row in retained if row["地点状态"] == "visited"]
    visited_mode_counts = Counter((row["移动方式"] or "unspecified") for row in visited)
    all_metrics = []
    for state in STATES:
        all_metrics.append({
            "section": "relation_state", "category": state, "relation_count": state_counts[state],
            "share_of_retained_relations": round(state_counts[state] / len(retained), 6),
            "definition": "Signed retained text-place relations, not a count of journeys or destinations.",
        })
    for mode in MODE_ORDER:
        all_metrics.append({
            "section": "mobility_mode_all_relations", "category": mode, "relation_count": mode_counts[mode],
            "share_of_retained_relations": round(mode_counts[mode] / len(retained), 6),
            "definition": "Coded mode attached to a retained text-place relation; repeated relations may belong to one narrated trip.",
        })
        all_metrics.append({
            "section": "mobility_mode_visited_relations", "category": mode, "relation_count": visited_mode_counts[mode],
            "share_of_visited_relations": round(visited_mode_counts[mode] / len(visited), 6),
            "definition": "Coded mode among signed retained visited relations only.",
        })
    write_csv(args.output_dir / "rq2_mobility_baseline_metrics.csv", all_metrics,
              ["section", "category", "relation_count", "share_of_retained_relations", "share_of_visited_relations", "definition"])

    era_rows = []
    for era in ERAS:
        era_relations = [row for row in retained if row["年代"] == era]
        for state in STATES:
            count = sum(row["地点状态"] == state for row in era_relations)
            era_rows.append({"era": era, "dimension": "relation_state", "category": state, "relation_count": count,
                             "share_within_era": round(count / len(era_relations), 6)})
        for mode in MODE_ORDER:
            count = sum((row["移动方式"] or "unspecified") == mode for row in era_relations)
            era_rows.append({"era": era, "dimension": "mobility_mode", "category": mode, "relation_count": count,
                             "share_within_era": round(count / len(era_relations), 6)})
    write_csv(args.output_dir / "rq2_mobility_by_era.csv", era_rows,
              ["era", "dimension", "category", "relation_count", "share_within_era"])

    sequences = sequence_metrics(retained)
    sequence_rows = [
        {"metric": "signed_retained_relations", "value": len(retained), "definition": "Q2 signed relation denominator."},
        {"metric": "texts_with_any_ordered_node", "value": sequences["texts_with_any_ordered_node"], "definition": "Texts with at least one numeric narrative route-order field."},
        {"metric": "ordered_relation_rows", "value": sequences["ordered_relation_rows"], "definition": "Retained relation rows carrying a numeric route-order field."},
        {"metric": "texts_with_two_or_more_ordered_nodes", "value": sequences["texts_with_two_or_more_ordered_nodes"], "definition": "Texts supporting at least one ordered narrative transition."},
        {"metric": "conservative_adjacent_narrative_transitions", "value": sequences["conservative_adjacent_narrative_transitions"], "definition": "Sum of distinct ordered nodes minus one within each eligible text; not a verified transport network."},
    ]
    write_csv(args.output_dir / "rq2_narrative_sequence_coverage.csv", sequence_rows, ["metric", "value", "definition"])

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    figure, axis = plt.subplots(figsize=(7.7, 4.8))
    bottoms = [0] * len(ERAS)
    colors = {"visited": "#2D6C91", "mentioned": "#B78B40", "imagined_or_compared": "#8E5A99", "uncertain": "#A0A0A0"}
    for state in STATES:
        values = [sum(row["年代"] == era and row["地点状态"] == state for row in retained) for era in ERAS]
        axis.bar(ERAS, values, bottom=bottoms, label=state, color=colors[state], width=0.68)
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]
    axis.set_title("Relation states by era in the signed Q2 baseline", loc="left", weight="bold")
    axis.set_ylabel("Retained text-place relations")
    axis.legend(frameon=False, ncols=2, loc="upper left")
    axis.spines[["top", "right"]].set_visible(False)
    figure.text(0.98, 0.015, "479 retained relations · archive profile, not population trend",
                ha="right", va="bottom", color="#4E4A52", fontsize=9)
    figure.tight_layout(rect=[0, 0.035, 1, 1])
    figure.savefig(args.figure_dir / "q2_relation_states_by_era_20261025.svg", format="svg")
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(7.8, 4.8))
    visible_modes = [mode for mode in MODE_ORDER if mode_counts[mode] > 0]
    bars = axis.barh(visible_modes[::-1], [mode_counts[mode] for mode in visible_modes[::-1]], color="#5B4B8A")
    axis.set_title("Mobility modes coded on signed Q2 relations", loc="left", weight="bold")
    axis.set_xlabel("Retained text-place relations")
    for bar in bars:
        axis.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2, str(int(bar.get_width())), va="center")
    axis.set_xlim(0, max(mode_counts.values()) * 1.15)
    axis.spines[["top", "right"]].set_visible(False)
    figure.text(0.98, 0.015, "One trip may yield several relation rows",
                ha="right", va="bottom", color="#4E4A52", fontsize=9)
    figure.tight_layout(rect=[0, 0.035, 1, 1])
    figure.savefig(args.figure_dir / "q2_mobility_modes_20261025.svg", format="svg")
    plt.close(figure)

    summary = {
        "release_date": "2026-10-25",
        "signed_relation_universe": len(relations),
        "retained_relations": len(retained),
        "paused_relations": decisions["暂停"],
        "visited_relations": state_counts["visited"],
        "non_arrival_relations": len(retained) - state_counts["visited"],
        "visited_relations_with_explicit_mobility_mode": len(visited) - visited_mode_counts["unspecified"],
        "relation_states": dict(state_counts),
        "mobility_modes": dict(mode_counts),
        "narrative_sequence_coverage": sequences,
        "interpretation_boundary": "Counts are relation-level coded evidence in the frozen archive. They do not count trips, reconstruct routes, or establish historical population trends.",
    }
    (args.output_dir / "rq2_mobility_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
