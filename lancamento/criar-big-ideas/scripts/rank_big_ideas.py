#!/usr/bin/env python3
"""Rank Big Ideas from real respondent scores stored in CSV."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path


METRICS = ("attention", "curiosity", "relevance", "credibility", "action_intent")


def load_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"idea_id", "respondent_id", *METRICS}
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise ValueError(f"missing columns: {', '.join(sorted(missing))}")
    parsed = []
    for line_no, row in enumerate(rows, start=2):
        if not row["idea_id"].strip() or not row["respondent_id"].strip():
            continue
        values = {}
        for metric in METRICS:
            raw = row[metric].strip()
            if not raw:
                raise ValueError(f"line {line_no}: empty score for {metric}")
            value = float(raw)
            if not 0 <= value <= 10:
                raise ValueError(f"line {line_no}: {metric} must be between 0 and 10")
            values[metric] = value
        parsed.append({"idea_id": row["idea_id"].strip(), "respondent_id": row["respondent_id"].strip(), **values})
    if not parsed:
        raise ValueError("no complete observations found")
    return parsed


def rank(rows: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["idea_id"]].append(row)
    report = []
    for idea_id, observations in grouped.items():
        metric_means = {metric: round(statistics.fmean(row[metric] for row in observations), 2) for metric in METRICS}
        respondent_count = len({row["respondent_id"] for row in observations})
        report.append({
            "idea_id": idea_id,
            "observations": len(observations),
            "respondents": respondent_count,
            **metric_means,
            "mean": round(statistics.fmean(metric_means.values()), 2),
        })
    return sorted(report, key=lambda item: (-item["mean"], -item["credibility"], item["idea_id"]))


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank Big Ideas using real 0-10 respondent scores.")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        results = rank(load_rows(args.csv_file))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("Rank | Idea | N | Mean | Attention | Curiosity | Relevance | Credibility | Action")
        for index, item in enumerate(results, start=1):
            print(
                f"{index} | {item['idea_id']} | {item['respondents']} | {item['mean']:.2f} | "
                f"{item['attention']:.2f} | {item['curiosity']:.2f} | {item['relevance']:.2f} | "
                f"{item['credibility']:.2f} | {item['action_intent']:.2f}"
            )
        print("\nScores summarize the supplied sample; they do not prove future performance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
