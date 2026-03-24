#!/usr/bin/env python3
"""Validate a repository that uses the project-memory layout."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

BUG_HEADER_RE = re.compile(r"^### \d{4}-\d{2}-\d{2} - .+$")
DECISION_HEADER_RE = re.compile(r"^### ADR-(\d{3}): .+ \(\d{4}-\d{2}-\d{2}\)$")
ISSUE_HEADER_RE = re.compile(r"^### \d{4}-\d{2}-\d{2} - [A-Za-z0-9._-]+: .+$")
WEEKLY_ISSUE_HEADER_RE = re.compile(r"^### Week of ")
STATUS_LINE_RE = re.compile(r"^- \*\*Status\*\*:")
PROJECT_MEMORY_HINT_RE = re.compile(r"(?i)(project memory system|docs/project_notes/)")
SECRET_ALLOW_HINT_RE = re.compile(
    r"(?i)(stored in|secret location|location|secret manager|password manager|vault|\.env|environment variable|email only|do not record|not in git)"
)
SECRET_GENERIC_RE = re.compile(r"(?i)\b(password|secret|token|api[- ]?key)\b")
SECRET_SPECIFIC_PATTERNS = {
    "private-key-block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "credentialed-dsn": re.compile(r"://[^/\s:@]+:[^/\s@]+@"),
    "shell-secret-placeholder": re.compile(r"\$\{[A-Z0-9_]+\}"),
    "github-token": re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "google-api-key": re.compile(r"\bAIza[0-9A-Za-z\-_]{20,}\b"),
    "openai-key": re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
}
RELATED_FILE_RE = re.compile(r"`([^`]+\.md)`")
ARCHITECTURE_SECTION_RE = re.compile(r"^## (.+)$")
INSTRUCTION_FILES = [
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path(".github/copilot-instructions.md"),
]
REQUIRED_MEMORY_FILES = ["bugs.md", "decisions.md", "key_facts.md", "issues.md"]
OPTIONAL_MEMORY_FILES = ["architecture.md"]
KNOWN_MEMORY_FILES = set(REQUIRED_MEMORY_FILES + OPTIONAL_MEMORY_FILES)
ARCHITECTURE_SECTION_NAMES = [
    "System Overview",
    "Component Map",
    "Key Entry Points",
    "Critical Flows",
    "Known Gotchas",
]
ENTRY_WARNING_LIMITS = {
    "bugs.md": 25,
    "decisions.md": 25,
    "issues.md": 40,
}
LARGE_MEMORY_THRESHOLD = 10


@dataclass
class Message:
    severity: str
    code: str
    path: str
    line: int | None
    message: str


class ValidationState:
    def __init__(self) -> None:
        self.messages: list[Message] = []

    def add(self, severity: str, code: str, path: Path, message: str, line: int | None = None) -> None:
        self.messages.append(
            Message(
                severity=severity,
                code=code,
                path=str(path),
                line=line,
                message=message,
            )
        )

    @property
    def errors(self) -> list[Message]:
        return [message for message in self.messages if message.severity == "error"]

    @property
    def warnings(self) -> list[Message]:
        return [message for message in self.messages if message.severity == "warning"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a repository that uses the project-memory layout.",
        epilog="Exit codes: 0 = validation passed, 1 = validation errors, 2 = usage or runtime error.",
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Repository root to validate (default: current directory)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--fail-on-warnings",
        action="store_true",
        help="Return a non-zero exit code when warnings are present.",
    )
    return parser.parse_args()


def iter_lines(path: Path, *, skip_fenced_code: bool = False) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    in_fenced_block = False

    for index, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.rstrip("\n")
        if skip_fenced_code and line.strip().startswith("```"):
            in_fenced_block = not in_fenced_block
            continue
        if skip_fenced_code and in_fenced_block:
            continue
        lines.append((index, line))

    return lines


def memory_dir(root: Path) -> Path:
    return root / "docs/project_notes"


def validate_required_files(root: Path, state: ValidationState) -> None:
    notes_dir = memory_dir(root)
    if not notes_dir.exists():
        state.add("error", "missing-memory-dir", notes_dir, "Missing docs/project_notes directory.")
        return
    if not notes_dir.is_dir():
        state.add("error", "memory-dir-not-dir", notes_dir, "docs/project_notes exists but is not a directory.")
        return

    for filename in REQUIRED_MEMORY_FILES:
        path = notes_dir / filename
        if not path.exists():
            state.add("error", "missing-memory-file", path, f"Missing required memory file: {filename}.")
        elif path.stat().st_size == 0:
            state.add("warning", "empty-memory-file", path, f"{filename} exists but is empty.")


def validate_bugs(root: Path, state: ValidationState) -> None:
    path = memory_dir(root) / "bugs.md"
    if not path.exists():
        return
    headers = [item for item in iter_lines(path, skip_fenced_code=True) if item[1].startswith("### ")]
    if not headers:
        state.add("warning", "no-bug-entries", path, "No bug entries found yet.")
    for line_no, line in headers:
        if not BUG_HEADER_RE.match(line):
            state.add(
                "error",
                "invalid-bug-header",
                path,
                "Bug entry headers must look like '### YYYY-MM-DD - Brief Description'.",
                line_no,
            )


def validate_decisions(root: Path, state: ValidationState) -> None:
    path = memory_dir(root) / "decisions.md"
    if not path.exists():
        return
    headers = [item for item in iter_lines(path, skip_fenced_code=True) if item[1].startswith("### ")]
    if not headers:
        state.add("warning", "no-adr-entries", path, "No ADR entries found yet.")
        return

    adr_numbers: list[int] = []
    lines = iter_lines(path, skip_fenced_code=True)
    for index, (line_no, line) in enumerate(lines):
        if not line.startswith("### "):
            continue
        match = DECISION_HEADER_RE.match(line)
        if not match:
            state.add(
                "error",
                "invalid-adr-header",
                path,
                "ADR headers must look like '### ADR-001: Title (YYYY-MM-DD)'.",
                line_no,
            )
            continue
        adr_numbers.append(int(match.group(1)))

        next_lines = [text for _, text in lines[index + 1 : index + 4] if text.strip()]
        if next_lines and not STATUS_LINE_RE.match(next_lines[0]):
            state.add(
                "warning",
                "missing-adr-status",
                path,
                "Consider adding a '- **Status**: ...' line immediately after each ADR header.",
                line_no,
            )

    if adr_numbers:
        if adr_numbers != sorted(adr_numbers):
            state.add("error", "adr-order", path, "ADR numbers should be strictly increasing.")
        if len(adr_numbers) != len(set(adr_numbers)):
            state.add("error", "adr-duplicate", path, "ADR numbers must be unique.")
        expected = list(range(min(adr_numbers), max(adr_numbers) + 1))
        if sorted(set(adr_numbers)) != expected:
            state.add(
                "warning",
                "adr-gap",
                path,
                "ADR numbering has gaps. Keep numbering sequential unless the project intentionally preserves historical gaps.",
            )


def validate_issues(root: Path, state: ValidationState) -> None:
    path = memory_dir(root) / "issues.md"
    if not path.exists():
        return
    headers = [item for item in iter_lines(path, skip_fenced_code=True) if item[1].startswith("### ")]
    if not headers:
        state.add("warning", "no-issue-entries", path, "No issue entries found yet.")
    for line_no, line in headers:
        if WEEKLY_ISSUE_HEADER_RE.match(line):
            state.add(
                "warning",
                "weekly-issues-format",
                path,
                "Weekly grouped issue headers are deprecated; prefer one dated entry per work item.",
                line_no,
            )
            continue
        if not ISSUE_HEADER_RE.match(line):
            state.add(
                "error",
                "invalid-issue-header",
                path,
                "Issue headers must look like '### YYYY-MM-DD - TICKET-ID: Brief Description'.",
                line_no,
            )


def validate_key_facts(root: Path, state: ValidationState) -> None:
    path = memory_dir(root) / "key_facts.md"
    if not path.exists():
        return
    for line_no, line in iter_lines(path, skip_fenced_code=True):
        stripped = line.strip()
        if not stripped:
            continue
        for code, pattern in SECRET_SPECIFIC_PATTERNS.items():
            if pattern.search(stripped):
                state.add(
                    "error",
                    code,
                    path,
                    "Suspicious secret-like content found in key_facts.md.",
                    line_no,
                )
        looks_like_fact_entry = stripped.startswith("-") and ":" in stripped
        if (
            looks_like_fact_entry
            and SECRET_GENERIC_RE.search(stripped)
            and not SECRET_ALLOW_HINT_RE.search(stripped)
        ):
            state.add(
                "warning",
                "generic-secret-hint",
                path,
                "This line mentions secret-like material without clearly treating it as a location-only reference.",
                line_no,
            )


def validate_architecture(root: Path, state: ValidationState) -> None:
    path = memory_dir(root) / "architecture.md"
    if not path.exists():
        return

    sections = [
        match.group(1).strip()
        for _, line in iter_lines(path, skip_fenced_code=True)
        if (match := ARCHITECTURE_SECTION_RE.match(line))
    ]
    if not sections:
        state.add(
            "warning",
            "no-architecture-sections",
            path,
            "architecture.md exists but does not contain any '## Section' headings.",
        )
        return

    missing = [section for section in ARCHITECTURE_SECTION_NAMES if section not in sections]
    if missing:
        state.add(
            "warning",
            "architecture-missing-sections",
            path,
            "Consider adding these architecture sections for better fresh-session orientation: "
            + ", ".join(missing)
            + ".",
        )


def validate_related_references(root: Path, state: ValidationState) -> None:
    notes_dir = memory_dir(root)
    if not notes_dir.exists() or not notes_dir.is_dir():
        return

    for path in sorted(notes_dir.glob("*.md")):
        for line_no, line in iter_lines(path, skip_fenced_code=True):
            if "**Related**:" not in line:
                continue
            references = RELATED_FILE_RE.findall(line)
            if not references:
                state.add(
                    "warning",
                    "invalid-related-line",
                    path,
                    "Related lines should include backticked markdown file references such as `bugs.md` or `decisions.md`.",
                    line_no,
                )
                continue
            for reference in references:
                if reference not in KNOWN_MEMORY_FILES:
                    state.add(
                        "warning",
                        "unknown-related-file",
                        path,
                        f"Related line references `{reference}`, which is not a known project-memory file.",
                        line_no,
                    )
                    continue
                target = notes_dir / reference
                if not target.exists():
                    state.add(
                        "warning",
                        "missing-related-target",
                        path,
                        f"Related line references `{reference}`, but that file does not exist in docs/project_notes.",
                        line_no,
                    )


def collect_entry_counts(root: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for filename in ENTRY_WARNING_LIMITS:
        path = memory_dir(root) / filename
        if not path.exists():
            counts[filename] = 0
            continue
        counts[filename] = sum(
            1 for _, line in iter_lines(path, skip_fenced_code=True) if line.startswith("### ")
        )
    return counts


def validate_memory_scale(root: Path, state: ValidationState) -> None:
    notes_dir = memory_dir(root)
    if not notes_dir.exists() or not notes_dir.is_dir():
        return

    entry_counts = collect_entry_counts(root)
    for filename, limit in ENTRY_WARNING_LIMITS.items():
        count = entry_counts.get(filename, 0)
        if count > limit:
            state.add(
                "warning",
                "many-memory-entries",
                notes_dir / filename,
                f"{filename} has {count} top-level entries. Consider stronger cross-links, summaries, or archive guidance to keep fresh sessions fast.",
            )

    total_entries = sum(entry_counts.values())
    architecture_path = notes_dir / "architecture.md"
    if total_entries >= LARGE_MEMORY_THRESHOLD and not architecture_path.exists():
        state.add(
            "warning",
            "missing-architecture-overview",
            notes_dir,
            "This repository has a large amount of project memory but no architecture.md overview. Consider adding one so fresh sessions can bootstrap quickly.",
        )


def validate_instruction_files(root: Path, state: ValidationState) -> None:
    existing = [path for path in INSTRUCTION_FILES if (root / path).exists()]
    if not existing:
        return

    hinted_files = []
    for relative_path in existing:
        path = root / relative_path
        if PROJECT_MEMORY_HINT_RE.search(path.read_text(encoding="utf-8")):
            hinted_files.append(relative_path)

    if not hinted_files:
        state.add(
            "warning",
            "missing-instruction-hint",
            root,
            "Instruction files exist but none mention docs/project_notes or Project Memory System.",
        )


def render_text(state: ValidationState) -> str:
    lines: list[str] = []
    for message in state.messages:
        location = message.path
        if message.line is not None:
            location = f"{location}:{message.line}"
        lines.append(f"{message.severity.upper():7} {location} [{message.code}] {message.message}")
    if not lines:
        lines.append("OK      validation passed with no issues.")
    lines.append("")
    lines.append(f"Summary: {len(state.errors)} error(s), {len(state.warnings)} warning(s).")
    return "\n".join(lines)


def render_json(root: Path, state: ValidationState) -> str:
    payload = {
        "root": str(root),
        "errors": [asdict(message) for message in state.errors],
        "warnings": [asdict(message) for message in state.warnings],
        "summary": {
            "errors": len(state.errors),
            "warnings": len(state.warnings),
            "passed": not state.errors,
        },
    }
    return json.dumps(payload, indent=2)


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Repository root does not exist: {root}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"Repository root is not a directory: {root}", file=sys.stderr)
        return 2

    state = ValidationState()
    validate_required_files(root, state)
    validate_bugs(root, state)
    validate_decisions(root, state)
    validate_issues(root, state)
    validate_key_facts(root, state)
    validate_architecture(root, state)
    validate_related_references(root, state)
    validate_memory_scale(root, state)
    validate_instruction_files(root, state)

    if args.format == "json":
        print(render_json(root, state))
    else:
        print(render_text(state))

    if state.errors:
        return 1
    if args.fail_on_warnings and state.warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
