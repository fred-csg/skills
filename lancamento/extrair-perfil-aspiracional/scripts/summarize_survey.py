#!/usr/bin/env python3
"""Summarize the structure and language of CSV, JSON or TXT survey data."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


TOKEN_RE = re.compile(r"[^\W\d_]+", re.UNICODE)
STOPWORDS = {
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos",
    "e", "em", "essa", "esse", "esta", "este", "eu", "foi", "mais", "mas",
    "me", "meu", "minha", "muito", "na", "nas", "no", "nos", "o", "os",
    "ou", "para", "pela", "pelo", "por", "que", "se", "sem", "ser", "sua",
    "seu", "tambem", "tem", "ter", "um", "uma", "voce"
}


def normalize(text: str) -> str:
    value = unicodedata.normalize("NFKD", text.casefold())
    return "".join(char for char in value if not unicodedata.combining(char))


def load_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.casefold()
    if suffix == ".csv":
        sample = path.read_text(encoding="utf-8-sig")
        try:
            dialect = csv.Sniffer().sniff(sample[:8192], delimiters=",;\t|")
            reader = csv.DictReader(io.StringIO(sample), dialect=dialect)
        except csv.Error:
            delimiter = max(",;\t|", key=sample[:8192].count)
            reader = csv.DictReader(io.StringIO(sample), delimiter=delimiter)
        return list(reader)
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            for key in ("responses", "respostas", "data", "dados"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break
        if not isinstance(data, list):
            raise ValueError("JSON must be a list or contain a responses/respostas/data/dados list")
        return [item if isinstance(item, dict) else {"response": item} for item in data]
    if suffix in {".txt", ".md"}:
        lines = [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        return [{"response": line} for line in lines]
    raise ValueError("Supported formats: .csv, .json, .txt and .md")


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("survey", type=Path)
    parser.add_argument("--top", type=int, default=20, help="Top terms per field")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    if args.top <= 0:
        parser.error("--top must be greater than zero")

    rows = load_rows(args.survey)
    columns = list(dict.fromkeys(key for row in rows for key in row))
    fields: dict[str, Any] = {}

    for column in columns:
        values = [stringify(row.get(column)) for row in rows]
        nonempty = [value for value in values if value]
        tokens = [normalize(token) for value in nonempty for token in TOKEN_RE.findall(value)]
        meaningful = [token for token in tokens if len(token) > 2 and token not in STOPWORDS]
        fields[column] = {
            "nonempty": len(nonempty),
            "missing": len(rows) - len(nonempty),
            "missing_percent": round((len(rows) - len(nonempty)) * 100 / len(rows), 2) if rows else None,
            "unique_nonempty": len(set(nonempty)),
            "average_words": round(sum(len(TOKEN_RE.findall(value)) for value in nonempty) / len(nonempty), 2) if nonempty else None,
            "top_terms": Counter(meaningful).most_common(args.top),
        }

    result = {
        "source": str(args.survey),
        "rows": len(rows),
        "columns": columns,
        "fields": fields,
        "caveat": "Term frequency is descriptive and requires contextual review; it does not establish psychological traits.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
