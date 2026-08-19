#!/usr/bin/env python3
"""Validate a structured objection-response library."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED = {
    "id", "category", "customer_wording", "status", "evidence", "response",
    "proof", "fit_limits", "cta", "alternative", "stage", "success_signal"
}
ALLOWED_STATUS = {"declarada", "inferencia", "inferência", "hipotese", "hipótese"}
RISK_PATTERNS = {
    "shame_or_insult": re.compile(r"pessoas (?:inteligentes|burras)|coisa sup[eé]rflua|vitim|med[ií]ocre", re.I),
    "false_urgency": re.compile(r"momento certo (?:é|e) um mito|enquanto voc[eê] pensa|nunca mais|decida agora|compre agora|feche hoje", re.I),
    "coercive_frame": re.compile(r"destruir obje[çc][aã]o|contra-ataque|ultimato|confronto brutal", re.I),
    "absolute_roi": re.compile(r"garantid[oa].{0,30}roi|vai se pagar|muda sua vida para sempre", re.I),
}


def load_items(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        data = data.get("objections", data.get("objecoes"))
    if not isinstance(data, list):
        raise ValueError("JSON must be a list or contain an objections/objecoes list")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("library", type=Path)
    args = parser.parse_args()
    items = load_items(args.library)
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()

    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            errors.append(f"item {index}: must be an object")
            continue
        missing = REQUIRED - item.keys()
        if missing:
            errors.append(f"item {index}: missing {sorted(missing)}")
            continue
        item_id = str(item["id"])
        if item_id in seen:
            errors.append(f"{item_id}: duplicate id")
        seen.add(item_id)
        status = str(item["status"]).casefold()
        if status not in ALLOWED_STATUS:
            errors.append(f"{item_id}: invalid status {status!r}")
        if not str(item["customer_wording"]).strip():
            errors.append(f"{item_id}: customer_wording is empty")
        if not str(item["evidence"]).strip():
            warnings.append(f"{item_id}: evidence is empty")
        if status != "declarada" and "hipótese" not in str(item["evidence"]).casefold() and "hipotese" not in str(item["evidence"]).casefold():
            warnings.append(f"{item_id}: non-declared objection should state how it will be validated")
        combined = " ".join(str(item.get(field, "")) for field in ("response", "cta", "alternative"))
        for label, pattern in RISK_PATTERNS.items():
            if pattern.search(combined):
                warnings.append(f"{item_id}: review {label}")

    result = {"valid": not errors, "objections": len(items), "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
