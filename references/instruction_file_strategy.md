# Instruction File Strategy

Use one shared memory system and avoid creating competing instruction files.

## Priority order

1. Update `AGENTS.md` when it already exists. This is the default shared file for Copilot-first repositories.
2. If `CLAUDE.md` also exists, keep its project-memory section aligned because the repository already opted into multiple agent files.
3. If `.github/copilot-instructions.md` already exists, update that file instead of creating a new Copilot-specific file.
4. If none of those files exist, ask before creating a new `AGENTS.md`.

## Editing rules

- Preserve repository-specific instructions that already exist in the file.
- Insert or refresh only the project-memory section; do not rewrite the whole document unless the user asks.
- Do not create both `AGENTS.md` and `CLAUDE.md` from scratch in the same pass.
- If the repository already maintains more than one instruction file, keep the project-memory guidance semantically aligned across them.
- If the repository already uses tool-specific files such as `.cursor/rules`, prefer adding a short pointer to `docs/project_notes/` rather than duplicating a large protocol block unless the user asks for a dedicated Cursor rule.

## Reusable section

Use `assets/shared_memory_protocol.md` as the starting point for the inserted memory section.
