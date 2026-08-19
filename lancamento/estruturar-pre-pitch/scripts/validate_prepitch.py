#!/usr/bin/env python3
"""Validate timing, disclosure and integrity of a structured pre-pitch."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TOP_REQUIRED = {
    "format", "total_duration_minutes", "pre_pitch_start", "pre_pitch_end",
    "offer_disclosure", "decision_safeguards", "segments"
}
SEGMENT_REQUIRED = {
    "id", "start", "end", "phase", "driver", "purpose", "script",
    "evidence", "transition", "risk_mitigation"
}
ALLOWED_PHASES = {
    "abertura", "problema", "consequencia", "possibilidade", "mecanismo",
    "prova", "adequacao", "transicao"
}
RISK_PATTERNS = {
    "covert_selling": re.compile(r"sem (?:a pessoa|o prospect) perceber|prepara[çc][aã]o subliminar|pitch invis[ií]vel", re.I),
    "hypnosis": re.compile(r"hipnose|comando hipn[oó]tico|comando subliminar", re.I),
    "inevitable_decision": re.compile(r"decis[aã]o inevit[aá]vel|j[aá] vendid[oa]|n[aã]o tem chance|mera formalidade", re.I),
    "false_dilemma": re.compile(r"(?:s[oó]|apenas) duas escolhas|ou voc[eê].{0,70}ou aceita", re.I),
    "shame_or_extremes": re.compile(r"ferida real|antes miser[aá]vel|perdedores|destruir ilus[aã]o", re.I),
    "pressure": re.compile(r"explodir.{0,20}urg[eê]ncia|precisa comprar|como comprar.{0,20}n[aã]o se", re.I),
    "objection_erasure": re.compile(r"zero obje[çc][oõ]es|destruir obje[çc][oõ]es|sem resist[eê]ncia", re.I),
}


def as_float(value: Any, label: str, errors: list[str]) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        errors.append(f"{label}: must be numeric")
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prepitch", type=Path)
    args = parser.parse_args()
    data = json.loads(args.prepitch.read_text(encoding="utf-8-sig"))
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        errors.append("root must be an object")
        data = {}
    missing_top = TOP_REQUIRED - data.keys()
    if missing_top:
        errors.append(f"root missing {sorted(missing_top)}")

    total = as_float(data.get("total_duration_minutes"), "total_duration_minutes", errors)
    start = as_float(data.get("pre_pitch_start"), "pre_pitch_start", errors)
    end = as_float(data.get("pre_pitch_end"), "pre_pitch_end", errors)
    if None not in (total, start, end):
        if not 0 <= start < end <= total:
            errors.append("expected 0 <= pre_pitch_start < pre_pitch_end <= total_duration_minutes")

    disclosure = str(data.get("offer_disclosure", ""))
    if "oferta" not in disclosure.casefold():
        errors.append("offer_disclosure must explicitly mention the offer/oferta")
    if not str(data.get("decision_safeguards", "")).strip():
        errors.append("decision_safeguards must not be empty")

    segments = data.get("segments", [])
    if not isinstance(segments, list) or not segments:
        errors.append("segments must be a non-empty list")
        segments = []

    previous_end: float | None = None
    seen: set[str] = set()
    for index, segment in enumerate(segments, 1):
        if not isinstance(segment, dict):
            errors.append(f"segment {index}: must be an object")
            continue
        missing = SEGMENT_REQUIRED - segment.keys()
        if missing:
            errors.append(f"segment {index}: missing {sorted(missing)}")
            continue
        segment_id = str(segment["id"])
        if segment_id in seen:
            errors.append(f"{segment_id}: duplicate id")
        seen.add(segment_id)
        seg_start = as_float(segment["start"], f"{segment_id}.start", errors)
        seg_end = as_float(segment["end"], f"{segment_id}.end", errors)
        if None not in (seg_start, seg_end):
            if seg_start >= seg_end:
                errors.append(f"{segment_id}: start must be before end")
            if start is not None and end is not None and not (start <= seg_start and seg_end <= end):
                errors.append(f"{segment_id}: segment must stay inside pre-pitch window")
            if previous_end is not None and seg_start < previous_end:
                errors.append(f"{segment_id}: overlaps previous segment")
            previous_end = seg_end
        phase = str(segment["phase"]).casefold()
        if phase not in ALLOWED_PHASES:
            errors.append(f"{segment_id}: invalid phase {phase!r}")
        if not str(segment["evidence"]).strip():
            warnings.append(f"{segment_id}: evidence is empty; cite a source or use [FONTE NECESSÁRIA]")
        combined = " ".join(str(segment.get(field, "")) for field in SEGMENT_REQUIRED)
        for label, pattern in RISK_PATTERNS.items():
            if pattern.search(combined):
                warnings.append(f"{segment_id}: review {label}")

    if segments and str(segments[-1].get("phase", "")).casefold() != "transicao":
        errors.append("last segment must use phase 'transicao'")
    for label, pattern in RISK_PATTERNS.items():
        if pattern.search(disclosure + " " + str(data.get("decision_safeguards", ""))):
            warnings.append(f"root: review {label}")

    result = {
        "valid": not errors,
        "segments": len(segments),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
