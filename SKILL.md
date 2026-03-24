---
name: project-memory
description: Use this skill when you need to set up or maintain shared project memory in `docs/project_notes/`, bootstrap a fresh session on a large codebase from previously recorded context, search prior bugs/decisions/facts before exploring from scratch, or record durable non-secret knowledge so future sessions do not relearn it.
license: MIT
compatibility: Works best when the agent can read and write Markdown files in the target repository and run bundled Python 3 scripts. Prefer `AGENTS.md` for Copilot-first repos, but adapt to existing `CLAUDE.md` or `.github/copilot-instructions.md` when those are already the project standard.
---

# Project Memory

## When to Use This Skill

Use this skill when:

- The user asks to set up project memory, track decisions, log a bug fix, update key facts, or initialize a shared memory system.
- A fresh session should reuse previously recorded architecture, bugs, decisions, or non-secret facts before exploring a large or long-lived repository from scratch.
- The task would benefit from checking whether the repository already remembers a similar bug, decision, configuration fact, misunderstanding, or gotcha before you propose a solution.
- A completed task should be reflected in a lightweight shared work log because future sessions are likely to need it.

Do not use this skill for private scratch notes, secrets, or one-off personal task tracking.

## Keep Context Lean

Load only the files you need:

- Read `references/instruction_file_strategy.md` if the instruction-file choice is unclear or the repository uses more than one agent-instruction file.
- Read `references/large_codebase_patterns.md` when the repository is large, long-lived, a monorepo, or the user wants a fast orientation briefing before deeper exploration.
- Read the specific template in `references/` only for the memory file you are creating or normalizing.
- Read `assets/shared_memory_protocol.md` when inserting or refreshing a project-memory section in an instruction file.
- Read `references/quick_reference.md` only if the user wants a concise map of which file to update.
- Use `scripts/summarize_project_memory.py <project-root>` when you want a concise project-memory briefing before reading full files.
- Use `scripts/search_project_memory.py <project-root> <query>` when the task is topic-specific and you want to avoid loading every memory file.

## Core Workflow

### 1. Inspect the Project First

- Check whether `docs/project_notes/` already exists.
- Check which instruction files already exist: `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`.
- Preserve user-authored content. Prefer targeted edits over whole-file rewrites.

### 2. Bootstrap a Fresh Session Deliberately

When the user wants orientation, context reuse, or help on a large codebase:

- Check `docs/project_notes/architecture.md` first if it exists. Treat it as the fast-start system map for future sessions.
- Then read only the minimum additional memory that matches the task:
  - `decisions.md` for architectural constraints and superseded choices
  - `key_facts.md` for non-secret configuration facts
  - recent `bugs.md` entries for recurring failures or prior misunderstandings
  - recent `issues.md` entries for work-in-flight or handoff context
- Use `scripts/summarize_project_memory.py <project-root>` when you need a concise briefing before deeper repo exploration.
- Use `scripts/search_project_memory.py <project-root> <query>` when the topic is narrow and you want a fast topic-specific lookup.
- If project memory conflicts with newer evidence from the repository or external systems, call out the conflict instead of assuming the memory is current.

### 3. Choose Instruction Files Deliberately

- Prefer `AGENTS.md` for GitHub Copilot-first repositories.
- If `AGENTS.md` already exists, update it.
- If `CLAUDE.md` already exists, keep its project-memory guidance aligned.
- If `.github/copilot-instructions.md` already exists, update it instead of creating an extra Copilot-specific file.
- If none of those files exist, ask before creating a new `AGENTS.md`.
- Do not create multiple new instruction files in one pass.

### 4. Create or Normalize Memory Files

Ensure `docs/project_notes/` contains these core files:

- `bugs.md`
- `decisions.md`
- `key_facts.md`
- `issues.md`

For large, long-lived, or multi-component repositories, recommend or create this optional high-signal file when the user asks or the repository already uses it:

- `architecture.md`

Use these templates for missing files:

- `references/architecture_template.md` for `architecture.md`
- `references/bugs_template.md`
- `references/decisions_template.md`
- `references/key_facts_template.md`
- `references/issues_template.md`

When files already exist:

- Keep the existing structure if it is clear and useful.
- Normalize only the sections you touch.
- Avoid reformatting the whole file unless the user asked for cleanup or the current format blocks reliable maintenance.

### 5. Read Memory Before Answering

Before large-codebase exploration or architectural work:

- Check `docs/project_notes/architecture.md` first if present.
- Check `docs/project_notes/decisions.md` before proposing architecture or workflow changes.
- If an ADR already covers the topic, follow it or explicitly explain why revisiting it is warranted.

When a bug or failure looks familiar:

- Check `docs/project_notes/bugs.md`.
- Reuse proven fixes when they apply.
- If the file contains conflicting guidance, call that out instead of guessing.

When you need project configuration:

- Check `docs/project_notes/key_facts.md`.
- Treat it as non-secret reference material only.
- Prefer named secret locations over secret values.

When you need recent context or handoff information:

- Check `docs/project_notes/issues.md`.

### 6. Write Memory Carefully

After initial setup, update memory files only when:

- The user explicitly asks.
- The task clearly includes documentation or memory maintenance.
- A repository instruction file already says project memory must be updated as part of the workflow.

If an update would help but was not requested:

- Suggest the update briefly.
- Do not silently add retrospective documentation.

When a new lesson should help future sessions orient faster, write it in the smallest relevant place:

- `architecture.md` for stable system shape, component boundaries, key entry points, critical flows, and durable gotchas
- `bugs.md` for recurring or instructive failures
- `decisions.md` for durable choices and supersession history
- `key_facts.md` for frequently needed non-secret configuration facts
- `issues.md` for lightweight dated work history

Use these formatting rules:

- Dates are `YYYY-MM-DD`.
- Prefer short bullet lists over tables.
- Keep entries concise enough to scan quickly.
- Use `**Related**:` lines for cross-file references when helpful.
- Mark deprecated or superseded guidance explicitly instead of silently rewriting history.
- Never put secret values, credential payloads, or password-bearing DSNs in tracked files.

### 7. File-Specific Rules

#### `architecture.md`

- Use this file as the fast-start system map for large or long-lived repositories.
- Capture component responsibilities, key entry points, critical flows, durable gotchas, and change hazards.
- Keep it terse. This file should help a fresh session decide what to inspect next, not replace the codebase.
- Use `references/architecture_template.md` before creating or restructuring the file.

#### `bugs.md`

- Log recurring or instructive issues.
- Each entry should capture `Issue`, `Root Cause`, `Solution`, and `Prevention`.
- If a bug teaches a durable repo-level sharp edge, mirror a concise note in `architecture.md` when appropriate.
- Use `references/bugs_template.md` before creating a new file or normalizing the format.

#### `decisions.md`

- Use ADR headers like `ADR-001`.
- Include `Context`, `Decision`, `Alternatives Considered`, and `Consequences`.
- Keep old ADRs when decisions change; mark them as superseded instead of deleting them.
- If an ADR changes how future sessions should orient themselves, refresh `architecture.md` as well.
- Use `references/decisions_template.md` before creating or restructuring the file.

#### `key_facts.md`

- Store only non-secret facts: URLs, ports, project IDs, service-account emails, environment names, and secret locations.
- Never store passwords, tokens, private keys, raw connection strings with credentials, or shell placeholders that imply secret values.
- Keep the highest-signal facts near the top of each section because fresh sessions may skim this file quickly.
- Use `references/key_facts_template.md` before creating or expanding the file.

#### `issues.md`

- Use one dated entry per task, ticket, or work item.
- Do not switch to weekly grouped summaries unless the repository already uses them and the user wants to keep them.
- Promote durable lessons out of `issues.md` into `architecture.md`, `bugs.md`, or `decisions.md` when they will matter across sessions.
- Use `references/issues_template.md` before creating or normalizing the file.

### 8. Validate and Summarize Before Finishing

After setup or memory edits:

- Run `python3 scripts/validate_project_memory.py <project-root>` when the validator is available.
- Fix validation errors and rerun.
- If available, run `python3 scripts/summarize_project_memory.py <project-root>` after larger memory updates to sanity-check whether a fresh session would get a useful briefing.
- If validation or summary warnings matter to the user, mention them in your handoff.

## Success Criteria

This skill is successful when:

- The target repository has a usable `docs/project_notes/` directory with the four core files, plus `architecture.md` when the repository is large enough to benefit from a fast-start overview.
- The repository's relevant instruction file(s) point agents to that memory system without creating unnecessary duplicates.
- A fresh session can reuse memory to narrow exploration before diving into the full codebase.
- Memory entries stay concise, maintainable, and free of secrets.
- The agent checked project memory before making architecture, debugging, or configuration recommendations when that context was relevant.
