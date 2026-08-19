#!/usr/bin/env python3
"""Validate an Extração de Área de Conhecimento session JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


DOMAINS = {"PC", "CE", "IP", "DF", "AU", "CT", "RE", "OT", "PB"}
MODES = {"live", "async", "material", "focused"}
STATUSES = {"in_progress", "paused", "needs_validation", "completed"}
CONFIDENCE = {"expert_confirmed", "transcript_clear", "uncertain"}
INSIGHT_TYPES = {"explicit", "tacit", "inference", "hypothesis"}
INSIGHT_STATUSES = {"confirmed", "needs_confirmation", "contradicted"}
MAX_QUESTION = {
    "PC": 8,
    "CE": 6,
    "IP": 6,
    "DF": 4,
    "AU": 4,
    "CT": 4,
    "RE": 3,
    "OT": 3,
    "PB": 2,
}
QUESTION_RE = re.compile(r"^(PC|CE|IP|DF|AU|CT|RE|OT|PB)([123])_(\d{2})$")


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


def valid_question_id(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    match = QUESTION_RE.fullmatch(value)
    if not match:
        return False
    domain, _level, number = match.groups()
    return 1 <= int(number) <= MAX_QUESTION[domain]


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    session = data.get("session")
    if not isinstance(session, dict):
        return ["session deve ser um objeto"], warnings

    for field in ("id", "expert", "area", "goal"):
        if not str(session.get(field, "")).strip():
            errors.append(f"session.{field} é obrigatório")

    mode = session.get("mode")
    status = session.get("status")
    target = session.get("question_target")
    if mode not in MODES:
        errors.append(f"session.mode inválido: {mode!r}")
    if status not in STATUSES:
        errors.append(f"session.status inválido: {status!r}")
    if not isinstance(target, int) or not 1 <= target <= 25:
        errors.append("session.question_target deve ser inteiro entre 1 e 25")
    elif mode != "focused" and not 20 <= target <= 25:
        errors.append("sessão completa deve mirar entre 20 e 25 perguntas")

    required_domains = session.get("required_domains")
    if not isinstance(required_domains, list) or not required_domains:
        errors.append("session.required_domains deve ser uma lista não vazia")
        required_domains = []
    else:
        invalid_domains = sorted(set(required_domains) - DOMAINS)
        if invalid_domains:
            errors.append("domínios inválidos: " + ", ".join(invalid_domains))
        if len(required_domains) != len(set(required_domains)):
            errors.append("session.required_domains contém duplicatas")

    if not isinstance(session.get("privacy_boundaries"), list):
        errors.append("session.privacy_boundaries deve ser uma lista")

    answers = data.get("answers")
    if not isinstance(answers, list):
        errors.append("answers deve ser uma lista")
        answers = []

    question_ids: list[str] = []
    for index, answer in enumerate(answers):
        if not isinstance(answer, dict):
            errors.append(f"answers[{index}] deve ser um objeto")
            continue
        question_id = answer.get("question_id")
        if not valid_question_id(question_id):
            errors.append(f"answers[{index}].question_id inválido: {question_id!r}")
        else:
            question_ids.append(question_id)
        for field in ("question", "answer", "source"):
            if not str(answer.get(field, "")).strip():
                errors.append(f"answers[{index}].{field} é obrigatório")
        if answer.get("confidence") not in CONFIDENCE:
            errors.append(f"answers[{index}].confidence inválido")
        if not isinstance(answer.get("mapped_insights", []), list):
            errors.append(f"answers[{index}].mapped_insights deve ser uma lista")
        if not isinstance(answer.get("probes", []), list):
            errors.append(f"answers[{index}].probes deve ser uma lista")

    duplicates = sorted(qid for qid, count in Counter(question_ids).items() if count > 1)
    if duplicates:
        errors.append("perguntas principais duplicadas: " + ", ".join(duplicates))

    covered_domains = {qid[:2] for qid in question_ids}
    if status == "completed":
        if isinstance(target, int) and len(question_ids) < target:
            errors.append(
                f"sessão concluída com {len(question_ids)} respostas; meta declarada é {target}"
            )
        uncovered = sorted(set(required_domains) - covered_domains)
        if uncovered:
            errors.append("sessão concluída sem cobrir: " + ", ".join(uncovered))
        if len(question_ids) > 25:
            errors.append("sessão concluída excede o limite de 25 perguntas principais")

    insights = data.get("insights", [])
    if not isinstance(insights, list):
        errors.append("insights deve ser uma lista")
        insights = []
    insight_ids: list[str] = []
    answer_id_set = set(question_ids)
    for index, insight in enumerate(insights):
        if not isinstance(insight, dict):
            errors.append(f"insights[{index}] deve ser um objeto")
            continue
        insight_id = insight.get("id")
        if not isinstance(insight_id, str) or not re.fullmatch(r"INS-\d{3,}", insight_id):
            errors.append(f"insights[{index}].id inválido")
        else:
            insight_ids.append(insight_id)
        if insight.get("type") not in INSIGHT_TYPES:
            errors.append(f"insights[{index}].type inválido")
        if insight.get("status") not in INSIGHT_STATUSES:
            errors.append(f"insights[{index}].status inválido")
        if not str(insight.get("statement", "")).strip():
            errors.append(f"insights[{index}].statement é obrigatório")
        sources = insight.get("source_question_ids")
        if not isinstance(sources, list) or not sources:
            errors.append(f"insights[{index}].source_question_ids deve ser lista não vazia")
        else:
            unknown = sorted(set(sources) - answer_id_set)
            if unknown:
                errors.append(
                    f"insights[{index}] referencia perguntas ausentes: {', '.join(unknown)}"
                )
        if insight.get("type") in {"inference", "hypothesis"} and insight.get("status") == "confirmed":
            warnings.append(
                f"{insight_id or f'insights[{index}]'} está confirmado apesar de ser inferência/hipótese"
            )

    duplicate_insights = sorted(
        insight_id for insight_id, count in Counter(insight_ids).items() if count > 1
    )
    if duplicate_insights:
        errors.append("IDs de insight duplicados: " + ", ".join(duplicate_insights))

    gaps = data.get("gaps")
    if not isinstance(gaps, list):
        errors.append("gaps deve ser uma lista")
    elif status == "completed" and gaps:
        warnings.append("sessão concluída ainda possui gaps registrados")

    if not isinstance(data.get("checkpoints"), list):
        errors.append("checkpoints deve ser uma lista")

    uncertain = sum(1 for answer in answers if isinstance(answer, dict) and answer.get("confidence") == "uncertain")
    if status == "completed" and uncertain:
        warnings.append(f"sessão concluída contém {uncertain} resposta(s) incerta(s)")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session_file", type=Path, help="Caminho do session.json")
    args = parser.parse_args()
    try:
        data = load(args.session_file)
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
    print(f"OK: sessão válida ({len(warnings)} aviso(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
