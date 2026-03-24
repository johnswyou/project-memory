#!/usr/bin/env python3
"""Generate a concise summary from docs/project_notes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CORE_MEMORY_FILES = ["bugs.md", "decisions.md", "key_facts.md", "issues.md"]
OPTIONAL_MEMORY_FILES = ["architecture.md"]
SECTION_RE = re.compile(r"^## (.+)$")
ENTRY_RE = re.compile(r"^### (.+)$")
STATUS_RE = re.compile(r"^- \*\*Status\*\*:\s*(.+)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a concise briefing from docs/project_notes.",
        epilog="Exit codes: 0 = success, 1 = invalid input, 2 = runtime error.",
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Repository root to summarize (default: current directory)",
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
        default=3,
        help="Maximum items to include per list section (default: 3)",
    )
    return parser.parse_args()


def project_notes_dir(root: Path) -> Path:
    notes_dir = root / "docs/project_notes"
    if not notes_dir.exists():
        raise ValueError("docs/project_notes does not exist.")
    if not notes_dir.is_dir():
        raise ValueError("docs/project_notes exists but is not a directory.")
    return notes_dir


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def extract_sections(path: Path, limit: int) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    current_title: str | None = None
    current_items: list[str] = []

    def flush() -> None:
        nonlocal current_title, current_items
        if current_title is None:
            return
        sections.append({"title": current_title, "items": current_items[:limit]})

    for raw_line in read_lines(path):
        if match := SECTION_RE.match(raw_line):
            flush()
            current_title = match.group(1).strip()
            current_items = []
            continue

        if current_title is None:
            continue

        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            current_items.append(stripped[2:].strip())
        else:
            current_items.append(stripped)

    flush()
    return sections


def extract_entries(path: Path, limit: int) -> list[dict[str, str | None]]:
    lines = read_lines(path)
    entries: list[dict[str, str | None]] = []

    for index, raw_line in enumerate(lines):
        match = ENTRY_RE.match(raw_line)
        if not match:
            continue
        title = match.group(1).strip()
        status: str | None = None
        for candidate in lines[index + 1 : index + 4]:
            stripped = candidate.strip()
            if not stripped:
                continue
            if status_match := STATUS_RE.match(stripped):
                status = status_match.group(1).strip()
                break
        entries.append({"title": title, "status": status})
        if len(entries) >= limit:
            break

    return entries


def build_summary(root: Path, limit: int) -> dict[str, object]:
    notes_dir = project_notes_dir(root)
    files_present = [
        filename
        for filename in OPTIONAL_MEMORY_FILES + CORE_MEMORY_FILES
        if (notes_dir / filename).exists()
    ]
    missing_core_files = [
        filename for filename in CORE_MEMORY_FILES if not (notes_dir / filename).exists()
    ]

    architecture_sections: list[dict[str, object]] = []
    architecture_path = notes_dir / "architecture.md"
    if architecture_path.exists():
        architecture_sections = extract_sections(architecture_path, limit)

    key_fact_sections: list[dict[str, object]] = []
    key_facts_path = notes_dir / "key_facts.md"
    if key_facts_path.exists():
        key_fact_sections = extract_sections(key_facts_path, limit)

    recent_decisions: list[dict[str, str | None]] = []
    decisions_path = notes_dir / "decisions.md"
    if decisions_path.exists():
        recent_decisions = extract_entries(decisions_path, limit)

    recent_bugs: list[dict[str, str | None]] = []
    bugs_path = notes_dir / "bugs.md"
    if bugs_path.exists():
        recent_bugs = extract_entries(bugs_path, limit)

    recent_issues: list[dict[str, str | None]] = []
    issues_path = notes_dir / "issues.md"
    if issues_path.exists():
        recent_issues = extract_entries(issues_path, limit)

    return {
        "root": str(root),
        "memory_dir": str(notes_dir.relative_to(root)),
        "files_present": files_present,
        "missing_core_files": missing_core_files,
        "architecture_sections": architecture_sections,
        "recent_decisions": recent_decisions,
        "recent_bugs": recent_bugs,
        "recent_issues": recent_issues,
        "key_fact_sections": key_fact_sections,
    }


def render_text(summary: dict[str, object]) -> str:
    lines: list[str] = [f"Project memory summary for {summary['root']}", "", "Files present:"]
    for filename in summary["files_present"]:
        lines.append(f"- {filename}")

    missing_core_files = summary["missing_core_files"]
    if missing_core_files:
        lines.extend(["", "Missing core files:"])
        for filename in missing_core_files:
            lines.append(f"- {filename}")

    architecture_sections = summary["architecture_sections"]
    if architecture_sections:
        lines.extend(["", "Architecture overview:"])
        for section in architecture_sections:
            title = section["title"]
            items = section["items"]
            preview = "; ".join(items) if items else "(no details recorded)"
            lines.append(f"- {title}: {preview}")

    recent_decisions = summary["recent_decisions"]
    if recent_decisions:
        lines.extend(["", "Recent decisions:"])
        for entry in recent_decisions:
            title = entry["title"]
            status = entry["status"]
            suffix = f" [{status}]" if status else ""
            lines.append(f"- {title}{suffix}")

    recent_bugs = summary["recent_bugs"]
    if recent_bugs:
        lines.extend(["", "Recent bugs:"])
        for entry in recent_bugs:
            lines.append(f"- {entry['title']}")

    recent_issues = summary["recent_issues"]
    if recent_issues:
        lines.extend(["", "Recent work log entries:"])
        for entry in recent_issues:
            title = entry["title"]
            status = entry["status"]
            suffix = f" [{status}]" if status else ""
            lines.append(f"- {title}{suffix}")

    key_fact_sections = summary["key_fact_sections"]
    if key_fact_sections:
        lines.extend(["", "Key facts:"])
        for section in key_fact_sections:
            title = section["title"]
            items = section["items"]
            preview = "; ".join(items) if items else "(no facts recorded)"
            lines.append(f"- {title}: {preview}")

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
        summary = build_summary(root, args.limit)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error: failed to read project memory: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(summary, indent=2))
    else:
        print(render_text(summary))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
