#!/usr/bin/env python3
"""Audit a Markdown manuscript without modifying it."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


WORD_RE = re.compile(r"\b[\wÀ-ÖØ-öø-ÿ]+(?:[-’'][\wÀ-ÖØ-öø-ÿ]+)*\b", re.UNICODE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
PENDING_RE = re.compile(r"\[(?:FONTE NECESSÁRIA|CASO PENDENTE|DECISÃO DO AUTOR|VERIFICAR|TEXTO|TÍTULO|SUBTÍTULO|AUTOR)[^\]]*\]", re.IGNORECASE)


def audit(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    words = WORD_RE.findall(text)
    headings = [(len(level), title.strip()) for level, title in HEADING_RE.findall(text)]
    chapter_headings = [title for level, title in headings if level == 1 and re.search(r"\bcap[ií]tulo\b", title, re.IGNORECASE)]
    pending = PENDING_RE.findall(text)
    normalized = [re.sub(r"\s+", " ", title.casefold()) for _, title in headings]
    repeated = [title for title, count in Counter(normalized).items() if count > 1]
    chapter_words = []
    matches = list(re.finditer(r"^#\s+.*\bcap[ií]tulo\b.*$", text, re.MULTILINE | re.IGNORECASE))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chapter_words.append({"heading": match.group(0)[2:].strip(), "words": len(WORD_RE.findall(text[match.end():end]))})

    return {
        "file": str(path.resolve()),
        "words": len(words),
        "estimated_pages_at_275_words": round(len(words) / 275, 1),
        "headings": len(headings),
        "chapters": len(chapter_headings),
        "chapter_word_counts": chapter_words,
        "pending_markers": pending,
        "repeated_headings": repeated,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a UTF-8 Markdown manuscript.")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a readable report.")
    args = parser.parse_args()
    if not args.manuscript.is_file():
        parser.error(f"file not found: {args.manuscript}")
    report = audit(args.manuscript)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"File: {report['file']}")
        print(f"Words: {report['words']}")
        print(f"Estimated pages @ 275 words: {report['estimated_pages_at_275_words']}")
        print(f"Headings: {report['headings']}")
        print(f"Chapters: {report['chapters']}")
        for item in report["chapter_word_counts"]:
            print(f"  - {item['heading']}: {item['words']} words")
        print(f"Pending markers: {len(report['pending_markers'])}")
        for marker in report["pending_markers"]:
            print(f"  - {marker}")
        print(f"Repeated headings: {len(report['repeated_headings'])}")
        for heading in report["repeated_headings"]:
            print(f"  - {heading}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
