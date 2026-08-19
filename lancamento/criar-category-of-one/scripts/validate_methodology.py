#!/usr/bin/env python3
"""Validate a Category of One methodology manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROUTE_PHASES = {"dc": set(range(1, 5)), "context": set(range(1, 6))}
PHASE_STATUS = {"not_started", "in_progress", "review", "approved"}
CHECKPOINT_STATUS = {"pending", "approved", "changes_requested", "paused"}
INPUT_STATUS = {"provided", "partial", "missing", "not_applicable"}
CLAIM_STATUS = {"observed", "verified", "inferred", "hypothesis", "rejected"}
REGISTRATION_STATUS = {
    "unsearched",
    "preliminary_search",
    "legal_review_required",
    "registered",
}
RISKY_CLAIMS = {
    "exclusividade absoluta": r"\b([uú]nico no mundo|nenhum concorrente|imposs[ií]vel de copiar)\b",
    "prova científica absoluta": r"\b(cientificamente comprovad[oa]|evid[eê]ncia irrefut[aá]vel)\b",
    "métrica sem contexto": r"\b95% diferente|\b100% personalizado|\b10 ou 10\.000\b",
}


def load(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"arquivo não encontrado: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"JSON inválido na linha {exc.lineno}, coluna {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(data, dict):
        raise ValueError("a raiz deve ser um objeto JSON")
    return data


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    project = data.get("project")
    if not isinstance(project, dict) or not str(project.get("name", "")).strip():
        errors.append("project.name é obrigatório")

    route = data.get("route")
    expected_phases = ROUTE_PHASES.get(route)
    if expected_phases is None:
        errors.append(f"route inválida: {route!r}")
        expected_phases = set()

    inputs = data.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        errors.append("inputs deve ser uma lista não vazia")
    else:
        for index, item in enumerate(inputs):
            if not isinstance(item, dict):
                errors.append(f"inputs[{index}] deve ser um objeto")
                continue
            if not str(item.get("type", "")).strip():
                errors.append(f"inputs[{index}].type é obrigatório")
            if item.get("status") not in INPUT_STATUS:
                errors.append(f"inputs[{index}].status inválido")
            if item.get("status") in {"provided", "partial"} and not str(item.get("source", "")).strip():
                errors.append(f"inputs[{index}] fornecido/parcial exige source")

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
        if not isinstance(phase_id, int) or phase_id not in expected_phases:
            errors.append(f"phases[{index}].id incompatível com rota {route!r}")
            continue
        if phase_id in phase_map:
            errors.append(f"fase {phase_id} duplicada")
        phase_map[phase_id] = phase
        status = phase.get("status")
        checkpoint = phase.get("checkpoint")
        if status not in PHASE_STATUS:
            errors.append(f"fase {phase_id}: status inválido")
        if checkpoint not in CHECKPOINT_STATUS:
            errors.append(f"fase {phase_id}: checkpoint inválido")
        if status == "approved" and checkpoint != "approved":
            errors.append(f"fase {phase_id}: status approved exige checkpoint approved")
        if checkpoint == "approved":
            if not phase.get("approved_by") or not phase.get("approved_at"):
                errors.append(f"fase {phase_id}: aprovação exige approved_by e approved_at")
            for field in ("outputs", "evidence", "assumptions"):
                if not isinstance(phase.get(field), list):
                    errors.append(f"fase {phase_id}: {field} deve ser uma lista")
            if not phase.get("outputs"):
                errors.append(f"fase {phase_id}: aprovação exige output")

    missing_phases = sorted(expected_phases - set(phase_map))
    if missing_phases:
        errors.append("faltam fases: " + ", ".join(map(str, missing_phases)))

    for phase_id in sorted(expected_phases):
        if phase_map.get(phase_id, {}).get("status") == "approved":
            previous = [pid for pid in expected_phases if pid < phase_id]
            pending = [pid for pid in previous if phase_map.get(pid, {}).get("status") != "approved"]
            if pending:
                errors.append(
                    f"fase {phase_id} aprovada antes de: {', '.join(map(str, sorted(pending)))}"
                )

    category = data.get("category")
    if not isinstance(category, dict):
        errors.append("category deve ser um objeto")
        category = {}
    phase_one_approved = phase_map.get(1, {}).get("status") == "approved"
    if phase_one_approved:
        for field in (
            "reference_category",
            "twist",
            "twist_source",
            "candidate_name",
            "definition",
        ):
            if not str(category.get(field, "")).strip():
                errors.append(f"category.{field} é obrigatório após a fase 1")

    registration_status = category.get("registration_status")
    if registration_status not in REGISTRATION_STATUS:
        errors.append("category.registration_status inválido")
    if registration_status == "registered":
        for field in ("jurisdiction", "registry", "registration_number"):
            if not str(category.get(field, "")).strip():
                errors.append(f"marca registrada exige category.{field}")

    serialized = json.dumps(data, ensure_ascii=False)
    if "®" in serialized and registration_status != "registered":
        errors.append("símbolo ® exige registration_status registered e dados do registro")

    methodology = data.get("methodology")
    if not isinstance(methodology, dict):
        errors.append("methodology deve ser um objeto")
        methodology = {}
    architecture_phase = phase_map.get(2, {})
    if architecture_phase.get("status") == "approved":
        mechanism_count = methodology.get("mechanism_count")
        pillar_count = methodology.get("pillar_count")
        if not isinstance(mechanism_count, int) or not 3 <= mechanism_count <= 7:
            errors.append("fase 2 aprovada exige methodology.mechanism_count entre 3 e 7")
        if not isinstance(pillar_count, int) or not 3 <= pillar_count <= 7:
            errors.append("fase 2 aprovada exige methodology.pillar_count entre 3 e 7")

    claims = data.get("claims")
    if not isinstance(claims, list):
        errors.append("claims deve ser uma lista")
        claims = []
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claims[{index}] deve ser um objeto")
            continue
        if not str(claim.get("claim", "")).strip():
            errors.append(f"claims[{index}].claim é obrigatório")
        status = claim.get("status")
        if status not in CLAIM_STATUS:
            errors.append(f"claims[{index}].status inválido")
        if status == "verified" and not str(claim.get("source", "")).strip():
            errors.append(f"claims[{index}] verificada exige source")

    for label, pattern in RISKY_CLAIMS.items():
        if re.search(pattern, serialized, flags=re.IGNORECASE):
            warnings.append(f"revisar {label}; exigir escopo e evidência adequada")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Caminho do methodology-manifest.json")
    args = parser.parse_args()
    try:
        data = load(args.manifest)
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
