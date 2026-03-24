#!/usr/bin/env python3
"""Search docs/project_notes for topic-specific matches."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MEMORY_FILES = [
    "architecture.md",
    "bugs.md",
    "decisions.md",
    "key_facts.md",
    "issues.md",
]
HEADING_RE = re.compile(r"^(#{1,3})\s+(.+)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search docs/project_notes for a keyword or phrase.",
        epilog="Exit codes: 0 = success, 1 = invalid input, 2 = runtime error.",
    )
    parser.add_argument(
        "root",
        help="Repository root to search",
    )
    parser.add_argument(
        "query",
        help="Keyword or phrase to search for",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of matches to return (default: 20)",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Use case-sensitive matching.",
    )
    return parser.parse_args()


def project_notes_dir(root: Path) -> Path:
    notes_dir = root / "docs/project_notes"
    if not notes_dir.exists():
        raise ValueError("docs/project_notes does not exist.")
    if not notes_dir.is_dir():
        raise ValueError("docs/project_notes exists but is not a directory.")
    return notes_dir


def contains(text: str, query: str, case_sensitive: bool) -> bool:
    if case_sensitive:
        return query in text
    return query.lower() in text.lower()


def search_file(path: Path, root: Path, query: str, case_sensitive: bool) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    headings: list[str] = []

    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if match := HEADING_RE.match(raw_line):
            level = len(match.group(1))
            title = match.group(2).strip()
            while len(headings) >= level:
                headings.pop()
            headings.append(title)

        if not raw_line.strip():
            continue
        if not contains(raw_line, query, case_sensitive):
            continue

        matches.append(
            {
                "path": str(path.relative_to(root)),
                "line": line_no,
                "heading": " > ".join(headings),
                "text": raw_line.strip(),
            }
        )

    return matches


def render_text(query: str, matches: list[dict[str, object]], truncated: bool) -> str:
    if not matches:
        return f"No project-memory matches for {query!r}."

    lines = [f"Project memory matches for {query!r}", ""]
    for match in matches:
        heading = f" [{match['heading']}]" if match["heading"] else ""
        lines.append(f"{match['path']}:{match['line']}{heading} {match['text']}")
    if truncated:
        lines.extend(["", "Results truncated. Re-run with a higher --limit if you need more matches."])
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    if args.limit < 1:
        print("Error: --limit must be at least 1.", file=sys.stderr)
        return 1

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Error: repository root does not exist: {root}", file=sys.stderr)
        return 1
    if not root.is_dir():
        print(f"Error: repository root is not a directory: {root}", file=sys.stderr)
        return 1

    try:
        notes_dir = project_notes_dir(root)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        matches: list[dict[str, object]] = []
        for filename in MEMORY_FILES:
            path = notes_dir / filename
            if not path.exists():
                continue
            matches.extend(search_file(path, root, args.query, args.case_sensitive))
    except OSError as exc:
        print(f"Error: failed to read project memory: {exc}", file=sys.stderr)
        return 2

    truncated = len(matches) > args.limit
    matches = matches[: args.limit]

    if args.format == "json":
        payload = {
            "query": args.query,
            "matches": matches,
            "truncated": truncated,
        }
        print(json.dumps(payload, indent=2))
    else:
        print(render_text(args.query, matches, truncated))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
