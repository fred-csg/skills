#!/usr/bin/env python3
"""Validate a structured 30-day, 90-piece aspirational campaign."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED = {"id", "day", "slot", "stage", "format", "hook", "objective", "evidence", "cta", "intensity"}
STAGES = {
    range(1, 8): "despertar",
    range(8, 15): "desejo",
    range(15, 23): "visao",
    range(23, 31): "compromisso",
}
RISK_PATTERNS = {
    "obsession_or_desperation": re.compile(r"obsess|obcec|desesper|implor", re.I),
    "shame_or_superiority": re.compile(r"mediocr|vida pequena|vers[aã]o min[uú]scula|evolu[ií]dos", re.I),
    "existential_pressure": re.compile(r"morrer sem|vida desperdi[çc]ada|nunca volta", re.I),
    "envy_or_fomo": re.compile(r"inveja|ficar para tr[aá]s|enquanto outros", re.I),
    "absolute_transformation": re.compile(r"mudar sua vida para sempre|potencial ilimitado|100% do seu potencial", re.I),
}


def expected_stage(day: int) -> str | None:
    return next((stage for days, stage in STAGES.items() if day in days), None)


def load_items(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        data = data.get("contents", data.get("conteudos"))
    if not isinstance(data, list):
        raise ValueError("JSON must be a list or contain a contents/conteudos list")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("campaign", type=Path)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    items = load_items(args.campaign)
    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()
    day_slots: Counter[tuple[int, int]] = Counter()

    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            errors.append(f"item {index}: must be an object")
            continue
        missing = REQUIRED - item.keys()
        if missing:
            errors.append(f"item {index}: missing {sorted(missing)}")
            continue
        item_id = str(item["id"])
        if item_id in seen_ids:
            errors.append(f"{item_id}: duplicate id")
        seen_ids.add(item_id)
        try:
            day, slot, intensity = int(item["day"]), int(item["slot"]), int(item["intensity"])
        except (TypeError, ValueError):
            errors.append(f"{item_id}: day, slot and intensity must be integers")
            continue
        if day not in range(1, 31) or slot not in range(1, 4):
            errors.append(f"{item_id}: day must be 1-30 and slot 1-3")
        if intensity not in range(1, 11):
            errors.append(f"{item_id}: intensity must be 1-10")
        stage = str(item["stage"]).casefold()
        if expected_stage(day) != stage:
            errors.append(f"{item_id}: day {day} expects stage {expected_stage(day)!r}, got {stage!r}")
        day_slots[(day, slot)] += 1
        combined = " ".join(str(item.get(field, "")) for field in ("hook", "objective", "cta"))
        for label, pattern in RISK_PATTERNS.items():
            if pattern.search(combined):
                warnings.append(f"{item_id}: review {label}")
        if not str(item["evidence"]).strip():
            warnings.append(f"{item_id}: evidence is empty; cite a source or use [FONTE NECESSÁRIA]")

    if not args.allow_partial:
        if len(items) != 90:
            errors.append(f"expected 90 contents, found {len(items)}")
        missing_slots: list[str] = []
        duplicate_slots: list[str] = []
        for day in range(1, 31):
            for slot in range(1, 4):
                count = day_slots[(day, slot)]
                if count == 0:
                    missing_slots.append(f"D{day:02d}-S{slot}")
                elif count > 1:
                    duplicate_slots.append(f"D{day:02d}-S{slot}({count}x)")
        if missing_slots:
            preview = ", ".join(missing_slots[:20])
            suffix = " ..." if len(missing_slots) > 20 else ""
            errors.append(f"missing {len(missing_slots)} slots: {preview}{suffix}")
        if duplicate_slots:
            errors.append(f"duplicate slots: {', '.join(duplicate_slots)}")

    result = {
        "valid": not errors,
        "contents": len(items),
        "days_present": sorted({int(item["day"]) for item in items if isinstance(item, dict) and str(item.get("day", "")).isdigit()}),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
