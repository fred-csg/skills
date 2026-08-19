#!/usr/bin/env python3
"""Validate a Construção de Lançamento Pro manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


VALID_CONTEXT = {"provided", "partial", "missing", "not_applicable"}
VALID_STATUS = {"not_started", "in_progress", "review", "approved"}
VALID_CHECKPOINT = {"pending", "approved", "changes_requested", "paused"}
DEPENDENCIES = {2: [1], 3: [2], 4: [3], 5: [4], 6: [3, 5], 7: [6], 8: [7], 9: [7, 8]}
REQUIRED_CONTEXT = {
    "expert_brief",
    "avatar_research",
    "market_research",
    "current_product",
    "launch_history",
    "resources",
}
RISKY_PATTERNS = {
    "garantia absoluta": r"\b(garantid[oa]|resultado inevit[aá]vel|funciona para (todos|qualquer um))\b",
    "escassez potencialmente artificial": r"\b([uú]ltimas vagas|[uú]ltima chance|antes que removam)\b",
    "alegação conspiratória": r"\b(conspira[cç][aã]o|documento vazado|n[aã]o quer que voc[eê] saiba)\b",
    "coerção emocional": r"\b(culpa|vergonha|vingan[cç]a|humilh|destruir obje[cç][aã]o)\b",
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"arquivo não encontrado: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido na linha {exc.lineno}, coluna {exc.colno}: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise ValueError("a raiz do manifesto deve ser um objeto JSON")
    return data


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    project = data.get("project")
    if not isinstance(project, dict) or not str(project.get("name", "")).strip():
        errors.append("project.name é obrigatório")

    context = data.get("context")
    if not isinstance(context, dict):
        errors.append("context deve ser um objeto")
    else:
        missing_keys = sorted(REQUIRED_CONTEXT - set(context))
        if missing_keys:
            errors.append("context sem campos: " + ", ".join(missing_keys))
        for key, value in context.items():
            if key in REQUIRED_CONTEXT and value not in VALID_CONTEXT:
                errors.append(f"context.{key} possui valor inválido: {value!r}")

    phases = data.get("phases")
    if not isinstance(phases, list):
        errors.append("phases deve ser uma lista")
        phases = []

    phase_map: dict[int, dict[str, Any]] = {}
    for index, phase in enumerate(phases):
        if not isinstance(phase, dict):
            errors.append(f"phases[{index}] deve ser um objeto")
            continue
        phase_id = phase.get("id")
        if not isinstance(phase_id, int) or phase_id not in range(1, 10):
            errors.append(f"phases[{index}].id deve ser inteiro entre 1 e 9")
            continue
        if phase_id in phase_map:
            errors.append(f"fase {phase_id} duplicada")
        phase_map[phase_id] = phase

        status = phase.get("status")
        checkpoint = phase.get("checkpoint")
        if status not in VALID_STATUS:
            errors.append(f"fase {phase_id}: status inválido: {status!r}")
        if checkpoint not in VALID_CHECKPOINT:
            errors.append(f"fase {phase_id}: checkpoint inválido: {checkpoint!r}")
        if status == "approved" and checkpoint != "approved":
            errors.append(f"fase {phase_id}: status approved exige checkpoint approved")
        if checkpoint == "approved":
            if not phase.get("approved_by") or not phase.get("approved_at"):
                errors.append(f"fase {phase_id}: aprovação exige approved_by e approved_at")
            for field in ("inputs", "outputs", "evidence", "assumptions", "risks"):
                if not isinstance(phase.get(field), list):
                    errors.append(f"fase {phase_id}: {field} deve ser uma lista")
            if not phase.get("outputs"):
                errors.append(f"fase {phase_id}: aprovação exige ao menos um output")

    absent = sorted(set(range(1, 10)) - set(phase_map))
    if absent:
        errors.append("faltam fases: " + ", ".join(map(str, absent)))

    for phase_id, dependencies in DEPENDENCIES.items():
        phase = phase_map.get(phase_id)
        if phase and phase.get("status") == "approved":
            for dependency in dependencies:
                if phase_map.get(dependency, {}).get("status") != "approved":
                    errors.append(f"fase {phase_id} aprovada antes da dependência {dependency}")

    inventory = data.get("inventory")
    if not isinstance(inventory, dict):
        errors.append("inventory deve ser um objeto")
    else:
        content_count = inventory.get("content_count")
        ad_count = inventory.get("ad_count")
        if not isinstance(content_count, int) or content_count < 0:
            errors.append("inventory.content_count deve ser inteiro não negativo")
        if not isinstance(ad_count, int) or ad_count < 0:
            errors.append("inventory.ad_count deve ser inteiro não negativo")
        if phase_map.get(8, {}).get("status") == "approved" and content_count != 84:
            errors.append("fase 8 aprovada exige exatamente 84 conteúdos")
        if phase_map.get(9, {}).get("status") == "approved" and ad_count != 100:
            errors.append("fase 9 aprovada exige exatamente 100 anúncios")

    claims = data.get("claims", [])
    if not isinstance(claims, list):
        errors.append("claims deve ser uma lista")
        claims = []
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claims[{index}] deve ser um objeto")
            continue
        if claim.get("status") == "verified" and not str(claim.get("source", "")).strip():
            errors.append(f"claims[{index}]: alegação verificada exige source")

    searchable = json.dumps(data, ensure_ascii=False)
    for label, pattern in RISKY_PATTERNS.items():
        if re.search(pattern, searchable, flags=re.IGNORECASE):
            warnings.append(f"revisar {label}; confirme evidência, contexto e autonomia do público")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Caminho do launch-manifest.json")
    args = parser.parse_args()
    try:
        data = load_json(args.manifest)
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate(data)
    for warning in warnings:
        print(f"AVISO: {warning}")
    for error in errors:
        print(f"ERRO: {error}")
    if errors:
        print(f"FALHOU: {len(errors)} erro(s), {len(warnings)} aviso(s)")
        return 1
    print(f"OK: manifesto válido ({len(warnings)} aviso(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
