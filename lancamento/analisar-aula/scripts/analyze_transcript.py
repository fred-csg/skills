#!/usr/bin/env python3
"""Generate reproducible lexical indicators from a Portuguese transcript."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


TOKEN_RE = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)?", re.UNICODE)
TIMESTAMP_RE = re.compile(r"(?<!\d)(?:(\d{1,2}):)?([0-5]?\d):([0-5]\d)(?!\d)")

GROUPS = {
    "first_person": {"eu", "meu", "minha", "meus", "minhas", "comigo"},
    "audience_focus": {"voce", "voces", "seu", "sua", "seus", "suas", "te", "ti", "contigo"},
    "cta_candidates": {"clique", "acesse", "compre", "inscreva", "cadastre", "garanta", "aplique"},
    "urgency_candidates": {"agora", "hoje", "urgente", "prazo", "encerra", "ultima", "ultimas"},
    "scarcity_candidates": {"escasso", "escassez", "limitado", "limitada", "vagas", "restam", "exclusivo", "exclusiva"},
    "emotional_load_candidates": {"devastador", "devastadora", "revolucionario", "revolucionaria", "secreto", "secreta", "transformador", "transformadora"},
    "superlative_candidates": {"melhor", "maior", "menor", "unico", "unica", "jamais", "nunca", "sempre"},
}


def normalize(token: str) -> str:
    decomposed = unicodedata.normalize("NFKD", token.casefold())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def timestamp_seconds(match: re.Match[str]) -> int:
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    return hours * 3600 + minutes * 60 + seconds


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcript", type=Path, help="UTF-8 text transcript")
    parser.add_argument("--duration-minutes", type=float, help="Known duration in minutes")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    if args.duration_minutes is not None and args.duration_minutes <= 0:
        parser.error("--duration-minutes must be greater than zero")

    text = args.transcript.read_text(encoding="utf-8-sig")
    raw_tokens = TOKEN_RE.findall(text)
    tokens = [normalize(token) for token in raw_tokens]
    counts = Counter(tokens)

    timestamps = [timestamp_seconds(match) for match in TIMESTAMP_RE.finditer(text)]
    inferred_duration = max(timestamps) / 60 if timestamps else None
    duration = args.duration_minutes if args.duration_minutes is not None else inferred_duration

    grouped = {
        name: {"total": sum(counts[word] for word in words), "terms": {word: counts[word] for word in sorted(words) if counts[word]}}
        for name, words in GROUPS.items()
    }
    first = grouped["first_person"]["total"]
    audience = grouped["audience_focus"]["total"]
    focus_total = first + audience

    result = {
        "source": str(args.transcript),
        "characters": len(text),
        "words": len(tokens),
        "unique_words": len(counts),
        "timestamp_count": len(timestamps),
        "duration_minutes": round(duration, 3) if duration is not None else None,
        "duration_source": "argument" if args.duration_minutes is not None else ("largest_timestamp" if timestamps else None),
        "words_per_minute": round(len(tokens) / duration, 2) if duration else None,
        "groups": grouped,
        "focus_ratio": {
            "first_person_percent": round(first * 100 / focus_total, 2) if focus_total else None,
            "audience_focus_percent": round(audience * 100 / focus_total, 2) if focus_total else None,
            "denominator": focus_total,
        },
        "caveat": "Lexical candidates require contextual human review; they do not prove persuasion or audience impact.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
