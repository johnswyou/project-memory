## Project Memory System

This repository keeps shared project memory in `docs/project_notes/` so humans and agents can reuse earlier fixes, architecture notes, decisions, and project facts instead of rediscovering them every session.

### Memory files

- `bugs.md` - recurring or instructive bugs, their fixes, and prevention notes
- `decisions.md` - ADRs and decision status changes
- `key_facts.md` - important non-secret project facts
- `issues.md` - lightweight dated work log
- `architecture.md` - optional but recommended for large or long-lived repos; fast orientation, component map, critical flows, and durable gotchas

### Working rules

- For a fresh session on a large repo, start with `architecture.md` if it exists.
- Check `decisions.md` before proposing architecture changes.
- Check `bugs.md` when an issue looks familiar.
- Check `key_facts.md` before guessing configuration.
- Check `issues.md` for recent work or handoff context when relevant.
- Update memory files when the user asks or when the task explicitly includes memory maintenance.
- Never store secrets, tokens, passwords, private keys, or password-bearing DSNs in tracked memory files.
