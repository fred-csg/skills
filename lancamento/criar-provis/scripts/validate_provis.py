#!/usr/bin/env python3
"""Validate structured PROVIs for evidence, safety and accessibility."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED = {
    "id", "name", "type", "concept", "claim", "claim_strength", "claim_limit",
    "priority", "moment", "educational_objective", "duration_seconds", "setup",
    "steps", "observation", "bridge", "materials", "evidence", "online",
    "in_person", "large_audience", "plan_b", "safety_level", "hazards",
    "mitigation", "consent", "accessibility", "phrases", "success_criterion"
}
ALLOWED_TYPES = {"experimento", "demonstracao", "demonstração", "analogia"}
ALLOWED_STRENGTHS = {"ilustrativo", "descritivo", "comparativo", "causal limitado"}
ALLOWED_SAFETY = {"baixo", "moderado", "alto"}
HAZARD_PATTERNS = {
    "fire_or_explosion": re.compile(r"chama|fogo|vela acesa|combust|explos", re.I),
    "electricity": re.compile(r"alta tens[aã]o|rede el[eé]trica|fio desencapado|choque el[eé]trico", re.I),
    "chemicals": re.compile(r"corrosiv|t[oó]xic|[aá]cido|solvente|reagente", re.I),
    "sharp_or_projectile": re.compile(r"vidro quebr|l[aâ]mina|faca|proj[eé]til|arma", re.I),
    "pressure": re.compile(r"pressuriz|v[aá]cuo improvisado", re.I),
    "body_or_ingestion": re.compile(r"ingerir|beber|inalar|aplicar na pele|conten[çc][aã]o", re.I),
    "animals": re.compile(r"animal|inseto vivo", re.I),
}
INTEGRITY_PATTERNS = {
    "analogy_as_proof": re.compile(r"(?:isso|isto) prova que", re.I),
    "inevitable_sale": re.compile(r"venda inevit[aá]vel|decis[aã]o inevit[aá]vel|vende sozinho", re.I),
    "objection_destruction": re.compile(r"destruir obje[çc][aã]o|imposs[ií]vel manter uma obje[çc][aã]o", re.I),
    "subliminal_command": re.compile(r"comando subliminar|hipn[oó]tic", re.I),
}


def load_items(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        data = data.get("provis")
    if not isinstance(data, list):
        raise ValueError("JSON must be a list or contain a provis list")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("provis", type=Path)
    args = parser.parse_args()
    items = load_items(args.provis)
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
        item_type = str(item["type"]).casefold()
        strength = str(item["claim_strength"]).casefold()
        safety = str(item["safety_level"]).casefold()
        if item_type not in ALLOWED_TYPES:
            errors.append(f"{item_id}: invalid type {item_type!r}")
        if strength not in ALLOWED_STRENGTHS:
            errors.append(f"{item_id}: invalid claim_strength {strength!r}")
        if safety not in ALLOWED_SAFETY:
            errors.append(f"{item_id}: invalid safety_level {safety!r}")
        if safety == "alto":
            errors.append(f"{item_id}: high-risk PROVI must be replaced by video, simulation or diagram")
        try:
            duration = int(item["duration_seconds"])
            if duration <= 0:
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"{item_id}: duration_seconds must be a positive integer")
        for field in ("steps", "materials", "hazards", "phrases"):
            if not isinstance(item[field], list):
                errors.append(f"{item_id}: {field} must be a list")
        if safety == "moderado" and (not item["hazards"] or not str(item["mitigation"]).strip()):
            errors.append(f"{item_id}: moderate risk requires hazards and mitigation")
        if item_type == "analogia" and strength != "ilustrativo":
            errors.append(f"{item_id}: analogy must use illustrative claim strength")
        if not str(item["claim_limit"]).strip():
            warnings.append(f"{item_id}: claim_limit is empty")
        if not str(item["evidence"]).strip():
            warnings.append(f"{item_id}: evidence is empty; cite a source or use [FONTE NECESSÁRIA]")
        if not str(item["accessibility"]).strip():
            warnings.append(f"{item_id}: accessibility is empty")
        combined = " ".join(str(item.get(field, "")) for field in REQUIRED)
        for label, pattern in HAZARD_PATTERNS.items():
            if pattern.search(combined):
                warnings.append(f"{item_id}: review hazard {label}")
        for label, pattern in INTEGRITY_PATTERNS.items():
            if pattern.search(combined):
                warnings.append(f"{item_id}: review integrity {label}")

    result = {"valid": not errors, "provis": len(items), "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
