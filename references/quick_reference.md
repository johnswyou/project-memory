# Project Memory Quick Reference

## Which file should I update?

- Recurring or instructive bug -> `docs/project_notes/bugs.md`
- Architecture or workflow choice that should survive across sessions -> `docs/project_notes/decisions.md`
- Important non-secret configuration fact -> `docs/project_notes/key_facts.md`
- Lightweight task or ticket log -> `docs/project_notes/issues.md`
- Fast orientation, system map, or “what new sessions should know first” context -> `docs/project_notes/architecture.md` (recommended for large or long-lived repos)

## What should I read first?

- Fresh session on a large repo -> `architecture.md` if present, then `decisions.md` and `key_facts.md`
- Topic-specific question -> `scripts/search_project_memory.py <root> <query>` when available, or read only the relevant memory file
- Familiar failure -> `bugs.md`
- Recent work or handoff context -> `issues.md`

## Which instruction file should I touch?

- Existing `AGENTS.md` first
- Existing `CLAUDE.md` too, if the repository already maintains it
- Existing `.github/copilot-instructions.md` instead of creating a second Copilot-specific file
- If none exist, ask before creating `AGENTS.md`

## Golden rules

- Read `architecture.md` first if present when starting fresh on large repos.
- Check memory before proposing architecture changes or debugging familiar failures.
- Keep entries dated and concise.
- Store secret locations, not secret values.
- Do not create multiple new instruction files in one pass.
