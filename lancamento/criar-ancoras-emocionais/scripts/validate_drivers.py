#!/usr/bin/env python3
"""Validate structured narrative drivers for completeness and pressure risks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED = {
    "id", "name", "function", "insight", "evidence", "mechanism", "stage",
    "opening", "story", "metaphor", "action", "phrases", "proof",
    "reinforcement", "alternative", "risk_mitigation"
}
RISK_PATTERNS = {
    "covert_conditioning": re.compile(r"instal(?:ar|e).{0,30}(?:mente|c[eé]rebro)|subliminar|hipnose|decis[aã]o inevit[aá]vel", re.I),
    "shame_or_wound": re.compile(r"dor vergonhosa|ferida reprimida|med[ií]ocre|vida pequena|expor a ferida", re.I),
    "fear_or_envy": re.compile(r"medo de perder|medo existencial|morrer (?:pres[oa]|sem)|inveja|quantos anos.{0,20}desperdi[çc]", re.I),
    "dependency": re.compile(r"mentor salvador|precisa de mim|s[oó] eu posso", re.I),
    "false_dilemma": re.compile(r"ou voc[eê].{0,60}ou aceita|n[aã]o existe outra op[çc][aã]o", re.I),
    "command_pressure": re.compile(r"compre agora|decida agora|aja antes que seja tarde", re.I),
    "absolute_claim": re.compile(r"resultado garantido|100% garantido|muda sua vida para sempre", re.I),
}


def load_items(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        data = data.get("drivers")
    if not isinstance(data, list):
        raise ValueError("JSON must be a list or contain a drivers list")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("drivers", type=Path)
    args = parser.parse_args()
    items = load_items(args.drivers)
    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()
    seen_names: set[str] = set()

    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            errors.append(f"item {index}: must be an object")
            continue
        missing = REQUIRED - item.keys()
        if missing:
            errors.append(f"item {index}: missing {sorted(missing)}")
            continue
        item_id = str(item["id"])
        name = str(item["name"]).strip()
        if item_id in seen_ids:
            errors.append(f"{item_id}: duplicate id")
        seen_ids.add(item_id)
        if name.casefold() in seen_names:
            errors.append(f"{item_id}: duplicate name {name!r}")
        seen_names.add(name.casefold())
        if not name or len(name.split()) > 3:
            errors.append(f"{item_id}: name must contain 1-3 words")
        phrases = item["phrases"]
        if not isinstance(phrases, list) or not 3 <= len(phrases) <= 5:
            errors.append(f"{item_id}: phrases must contain 3-5 items")
        if not str(item["evidence"]).strip() or not str(item["proof"]).strip():
            warnings.append(f"{item_id}: evidence/proof is empty; cite a source or use [FONTE NECESSÁRIA]")
        combined = " ".join(str(item.get(field, "")) for field in REQUIRED if field != "phrases")
        combined += " " + " ".join(str(value) for value in phrases) if isinstance(phrases, list) else ""
        for label, pattern in RISK_PATTERNS.items():
            if pattern.search(combined):
                warnings.append(f"{item_id}: review {label}")

    result = {"valid": not errors, "drivers": len(items), "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
