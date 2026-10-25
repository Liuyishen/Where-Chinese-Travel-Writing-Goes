#!/usr/bin/env python3
"""Build disclosure-safe signed RQ3 country coverage and concentration outputs."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from openpyxl import load_workbook


ERAS = ["1980s", "1990s", "2000s", "2010s", "2020s"]
WEIGHTED_CATEGORIES = {"中国国内", "当前国家", "当前国家对应"}


def sheet_rows(workbook, sheet_name, header_row=1):
    sheet = workbook[sheet_name]
    iterator = sheet.iter_rows(min_row=header_row, values_only=True)
    headers = next(iterator)
    return [dict(zip(headers, row)) for row in iterator if any(value not in (None, "") for value in row)]


def write_csv(path, rows, headers):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def shannon(counts):
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((count / total) * math.log(count / total) for count in counts.values() if count)


def gini(counts):
    values = sorted(counts.values())
    n = len(values)
    total = sum(values)
    if n < 2 or total == 0:
        return 0.0
    return round((2 * sum((i + 1) * value for i, value in enumerate(values)) / (n * total)) - (n + 1) / n, 6)


def concentration_metrics(counts):
    total = sum(counts.values())
    shares = sorted((count / total for count in counts.values()), reverse=True) if total else []
    entropy = shannon(counts)
    categories = len(counts)
    return {
        "relation_denominator": total,
        "country_units": categories,
        "shannon_entropy": round(entropy, 6),
        "normalized_shannon_entropy": round(entropy / math.log(categories), 6) if categories > 1 else 0.0,
        "hhi": round(sum(share * share for share in shares), 6),
        "gini": gini(counts),
        "top_1_share": round(shares[0], 6) if shares else 0.0,
        "top_3_share": round(sum(shares[:3]), 6) if shares else 0.0,
        "china_share": round(counts.get("中国", 0) / total, 6) if total else 0.0,
    }


def split_multi(value):
    return [item.strip() for item in str(value).split("；") if item.strip()]


def tidy_svg(path):
    """Keep generated SVGs free of trailing whitespace for reproducible diffs."""
    path.write_text("\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--relations-workbook", required=True, type=Path)
    parser.add_argument("--scope-workbook", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--figure-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.figure_dir.mkdir(parents=True, exist_ok=True)

    relation_book = load_workbook(args.relations_workbook, read_only=True, data_only=True)
    relations = sheet_rows(relation_book, "规范关系_410")
    reviews = {row["canonical_relationship_id"]: row for row in sheet_rows(relation_book, "关系AI复核与人工签署_20261006")}
    retained = [row for row in relations if reviews[row["canonical_relationship_id"]]["人工签署决定"] == "保留"]
    if len(retained) != 479:
        raise ValueError(f"Expected 479 signed retained relations, got {len(retained)}")

    scope_book = load_workbook(args.scope_workbook, read_only=True, data_only=True)
    scope_rows = sheet_rows(scope_book, "国家地区规范队列", header_row=5)
    scope = {}
    for row in scope_rows:
        raw = row["原始国家/地区值"]
        if row["人工签署决定"] not in {"保留", "修订"}:
            raise ValueError(f"Unsigned country treatment: {raw}")
        scope[raw] = {
            "unit": str(row["人工确认覆盖单元"] or "").strip(),
            "category": row["建议类别"],
            "handling": row["建议处理规则"],
        }

    weighted = []
    expanded_coverage = defaultdict(set)
    strict_coverage = defaultdict(set)
    excluded_counts = Counter()
    for relation in retained:
        raw = str(relation["国家地区"] or "（缺失）").strip() or "（缺失）"
        if raw not in scope:
            raise ValueError(f"No signed scope treatment for {raw}")
        decision = scope[raw]
        era = relation["年代"]
        if decision["category"] in WEIGHTED_CATEGORIES:
            if not decision["unit"]:
                raise ValueError(f"Weighted category lacks country unit: {raw}")
            entry = dict(relation)
            entry["q3_country_unit"] = decision["unit"]
            weighted.append(entry)
            strict_coverage[era].add(decision["unit"])
            expanded_coverage[era].add(decision["unit"])
        elif decision["category"] == "多国关系":
            expanded_coverage[era].update(split_multi(decision["unit"]))
            excluded_counts[decision["category"]] += 1
        else:
            excluded_counts[decision["category"]] += 1

    if len(weighted) != 467:
        raise ValueError(f"Expected 467 strict weighted relations, got {len(weighted)}")

    coverage_rows = []
    concentration_rows = []
    for era in ERAS:
        era_all = [row for row in retained if row["年代"] == era]
        era_weighted = [row for row in weighted if row["年代"] == era]
        counts = Counter(row["q3_country_unit"] for row in era_weighted)
        metrics = concentration_metrics(counts)
        coverage_rows.append({
            "era": era,
            "signed_retained_relations": len(era_all),
            "strict_country_weighted_relations": len(era_weighted),
            "excluded_non_country_or_multi_relations": len(era_all) - len(era_weighted),
            "strict_country_units": len(strict_coverage[era]),
            "strict_non_china_country_units": len(strict_coverage[era] - {"中国"}),
            "coverage_units_with_multi_country_sensitivity": len(expanded_coverage[era]),
            "non_china_units_with_multi_country_sensitivity": len(expanded_coverage[era] - {"中国"}),
            "definition": "Strict coverage uses only signed current-country units. Sensitivity adds multi-country components to unique coverage only, never to relation weights.",
        })
        concentration_rows.append({"era": era, **metrics, "definition": "Country distribution across strict weighted relations only; it is an archive profile, not a population trend."})
    write_csv(args.output_dir / "rq3_country_coverage_by_era.csv", coverage_rows,
              ["era", "signed_retained_relations", "strict_country_weighted_relations", "excluded_non_country_or_multi_relations", "strict_country_units", "strict_non_china_country_units", "coverage_units_with_multi_country_sensitivity", "non_china_units_with_multi_country_sensitivity", "definition"])
    write_csv(args.output_dir / "rq3_country_concentration_by_era.csv", concentration_rows,
              ["era", "relation_denominator", "country_units", "shannon_entropy", "normalized_shannon_entropy", "hhi", "gini", "top_1_share", "top_3_share", "china_share", "definition"])

    sensitivity_rows = []
    for status, label in [(None, "all_retained"), ("visited", "visited_only")]:
        subset = [row for row in retained if status is None or row["地点状态"] == status]
        subset_weighted = []
        for relation in subset:
            raw = str(relation["国家地区"] or "（缺失）").strip() or "（缺失）"
            decision = scope[raw]
            if decision["category"] in WEIGHTED_CATEGORIES:
                subset_weighted.append((relation, decision["unit"]))
        for era in ERAS:
            counts = Counter(unit for relation, unit in subset_weighted if relation["年代"] == era)
            metrics = concentration_metrics(counts)
            sensitivity_rows.append({"scope": label, "era": era, **metrics,
                                     "definition": "All-retained includes every signed retained relation; visited-only keeps only relations with place_state=visited. Both use strict country weighting."})
    write_csv(args.output_dir / "rq3_country_concentration_sensitivity.csv", sensitivity_rows,
              ["scope", "era", "relation_denominator", "country_units", "shannon_entropy", "normalized_shannon_entropy", "hhi", "gini", "top_1_share", "top_3_share", "china_share", "definition"])

    all_counts = Counter(row["q3_country_unit"] for row in weighted)
    summary = {
        "release_date": "2026-10-26",
        "signed_retained_relations": len(retained),
        "strict_country_weighted_relations": len(weighted),
        "excluded_relations_by_scope_category": dict(excluded_counts),
        "all_era_strict_concentration": concentration_metrics(all_counts),
        "interpretation_boundary": "Coverage and concentration describe the frozen archive after project-lead-signed country treatment. Multi-country relations expand coverage only in sensitivity analysis and never receive invented fractional relation weights. Results are not population trends, geopolitical core-periphery claims, or counts of actual trips.",
    }
    (args.output_dir / "rq3_country_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    figure, axis = plt.subplots(figsize=(7.8, 4.8))
    strict_non_china = [row["strict_non_china_country_units"] for row in coverage_rows]
    x = list(range(len(ERAS)))
    bars = axis.bar(x, strict_non_china, color="#2D6C91", width=0.62)
    for bar in bars:
        axis.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.35, str(int(bar.get_height())), ha="center", va="bottom")
    axis.set_xticks(x, ERAS)
    axis.set_ylabel("Non-China country units")
    axis.set_title("Non-China country coverage by archive era", loc="left", weight="bold")
    axis.spines[["top", "right"]].set_visible(False)
    figure.text(0.5, 0.015, "Multi-country sensitivity is identical in every era · coverage only, not a population trend", ha="center", va="bottom", color="#4E4A52", fontsize=9)
    figure.tight_layout(rect=[0, 0.035, 1, 1])
    coverage_figure = args.figure_dir / "rq3_non_china_country_coverage_20261026.svg"
    figure.savefig(coverage_figure, format="svg")
    tidy_svg(coverage_figure)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(7.8, 4.8))
    axis.plot(x, [row["china_share"] for row in concentration_rows], marker="o", linewidth=2.3, color="#5B4B8A", label="China relation share")
    axis.plot(x, [row["hhi"] for row in concentration_rows], marker="o", linewidth=2.3, color="#2F6B5F", label="HHI concentration")
    axis.set_xticks(x, ERAS)
    axis.set_ylim(0, 1)
    axis.set_ylabel("Share / index")
    axis.set_title("Country concentration in strict relation profiles", loc="left", weight="bold")
    axis.legend(frameon=False, loc="upper right")
    axis.spines[["top", "right"]].set_visible(False)
    figure.text(0.98, 0.015, "467 strict country-weighted relations overall", ha="right", va="bottom", color="#4E4A52", fontsize=9)
    figure.tight_layout(rect=[0, 0.035, 1, 1])
    concentration_figure = args.figure_dir / "rq3_country_concentration_20261026.svg"
    figure.savefig(concentration_figure, format="svg")
    tidy_svg(concentration_figure)
    plt.close(figure)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
