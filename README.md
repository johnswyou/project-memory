# Project Memory Skill

`project-memory` is an Agent Skill for setting up and maintaining shared repository memory in `docs/project_notes/`. Its main job is to help future sessions avoid relearning the same architecture, bugs, decisions, and non-secret configuration facts from scratch.

The skill keeps the original four-file memory model as the backward-compatible core:

- `bugs.md`
- `decisions.md`
- `key_facts.md`
- `issues.md`

For large or long-lived repositories, it also supports an optional `architecture.md` file as a fast orientation layer for fresh sessions.

## What the skill is intended to do

The skill is meant to help a repository remember things that would otherwise be rediscovered every session:

- `bugs.md` stores recurring or instructive bugs, their root causes, and proven fixes.
- `decisions.md` stores ADRs so future changes do not accidentally fight earlier architecture choices.
- `key_facts.md` stores important **non-secret** project facts such as ports, URLs, project IDs, and secret locations.
- `issues.md` stores a short work log that points back to tickets or issue trackers.
- `architecture.md` stores a concise system map, key entry points, critical flows, and durable gotchas for large or long-lived codebases.

It also teaches the active agent to check those files before making architecture or debugging recommendations, and to use bundled summary/search tooling when a fresh session needs a fast briefing.

## Intended workflow

1. Activate the skill when the user asks to set up project memory, record durable context, reuse previously learned context, or avoid exploring a large codebase from scratch.
2. Inspect the project for `docs/project_notes/` and for existing instruction files such as `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`.
3. Bootstrap orientation deliberately:
   - read `docs/project_notes/architecture.md` first if it exists
   - then read only the minimum task-relevant memory files
   - use the bundled summary/search scripts when they save context
4. Create any missing core memory files from the bundled templates.
5. Update the repository's relevant instruction file so future agent sessions know to consult project memory.
6. Use project memory before proposing architecture changes, guessing configuration, or debugging familiar issues.
7. Add or update memory entries when the user asks or when the task explicitly includes memory maintenance.
8. Validate the resulting memory layout with `scripts/validate_project_memory.py`.

## Large-codebase positioning

This skill is intentionally optimized for large or long-lived repositories where a new session can waste time and tokens rediscovering the same context repeatedly.

The core design choices are:

- keep `SKILL.md` lean and trigger-friendly
- use progressive disclosure through `references/` and `scripts/`
- preserve a simple Markdown-first memory model
- add a high-signal optional `architecture.md` instead of turning project memory into a giant knowledge dump
- provide agent-friendly scripts for summary and search so fresh sessions can orient quickly

## Instruction-file strategy

This skill is GitHub Copilot-first, but it avoids creating competing instruction files.

- If `AGENTS.md` exists, update it.
- If `CLAUDE.md` also exists, keep the memory section aligned there too.
- If `.github/copilot-instructions.md` already exists, update that instead of creating another Copilot-specific file.
- If none of those files exist, ask before creating a new `AGENTS.md`.
- Do not create multiple new instruction files in one pass.

See `references/instruction_file_strategy.md` for the detailed decision tree and `assets/shared_memory_protocol.md` for the reusable memory section.

## Quick start

Skill install locations vary by client. Common examples are `.agents/skills/`, `.claude/skills/`, or a repository-specific skills directory such as `.github/skills/`.

### Generic manual install

```bash
mkdir -p .agents/skills
cp -r project-memory .agents/skills/
```

### Claude-style manual install

```bash
mkdir -p .claude/skills
cp -r project-memory .claude/skills/
```

### Install with `skilz`

```bash
skilz install SpillwaveSolutions_project-memory/project-memory
```

After installation, confirm that the chosen skill directory contains `project-memory/SKILL.md`.

## Package layout

```text
project-memory/
├── SKILL.md
├── README.md
├── assets/
│   └── shared_memory_protocol.md
├── references/
│   ├── architecture_template.md
│   ├── bugs_template.md
│   ├── decisions_template.md
│   ├── instruction_file_strategy.md
│   ├── issues_template.md
│   ├── key_facts_template.md
│   ├── large_codebase_patterns.md
│   └── quick_reference.md
├── scripts/
│   ├── search_project_memory.py
│   ├── summarize_project_memory.py
│   └── validate_project_memory.py
├── evals/
│   ├── evals.json
│   ├── trigger-train.json
│   ├── trigger-validation.json
│   └── files/
└── examples/
    └── copilot-project/
```

The package follows the Agent Skills pattern: keep `SKILL.md` lean, move detailed guidance into `references/`, keep static reusable content in `assets/`, and bundle scripts only when they remove repeated work.

## Templates, references, and scripts

### Memory-file templates

The memory-file templates live in `references/`:

- `references/architecture_template.md`
- `references/bugs_template.md`
- `references/decisions_template.md`
- `references/key_facts_template.md`
- `references/issues_template.md`

### Additional reference material

- `references/instruction_file_strategy.md` explains which instruction file to update and when.
- `references/large_codebase_patterns.md` explains when and how to use the optional `architecture.md` fast-start layer.
- `references/quick_reference.md` gives a short “which file for which task” summary.
- `assets/shared_memory_protocol.md` is the reusable section to copy or adapt into repository instruction files.

### Bundled scripts

- `scripts/summarize_project_memory.py` generates a concise briefing from `docs/project_notes/`.
- `scripts/search_project_memory.py` finds topic-specific matches across project-memory files.
- `scripts/validate_project_memory.py` validates layout, heading formats, secret safety, related-file references, and large-memory hygiene warnings.

## Validation and evaluation

### Validate the skill package

If you have the Agent Skills reference tooling available, validate the package itself from the skill root:

```bash
skills-ref validate .
```

### Summarize or search project memory

```bash
python3 scripts/summarize_project_memory.py examples/copilot-project
python3 scripts/search_project_memory.py examples/copilot-project alembic
```

These scripts are meant for fresh sessions that need a fast orientation or a topic-specific lookup without loading every memory file into context.

### Validate a project that uses this memory layout

```bash
python3 scripts/validate_project_memory.py examples/copilot-project
```

The validator checks for the expected `docs/project_notes/` layout, canonical heading patterns, suspicious secret-like content in `key_facts.md`, broken related-file references, architecture-overview hygiene for larger memory sets, and whether at least one instruction file references project memory.

### Trigger-eval inputs

Use the bundled query sets when tuning the `description` field:

- `evals/trigger-train.json`
- `evals/trigger-validation.json`

These follow the official “should trigger / should not trigger” guidance and now cover session bootstrap, context reuse, and large-codebase orientation prompts in addition to the original memory-maintenance cases.

### Output-quality evals

`evals/evals.json` contains starter eval cases for:

- Copilot-first setup in a repository with `AGENTS.md`
- Consulting existing ADRs before proposing a conflicting architecture change
- Updating `key_facts.md` without leaking secrets
- Bootstrapping a fresh session on a larger repository from project memory before exploring the codebase
- Searching project memory for targeted historical auth context before proposing a fix

The goal is to compare with-skill runs against a baseline and refine the skill only where it clearly adds value.

## Example fixture

`examples/copilot-project/` is a small reference repository that shows the intended end state:

- `AGENTS.md` contains the shared project-memory protocol
- `docs/project_notes/` contains the four core files plus an optional `architecture.md`
- entries are concise, dated, and cross-referenced when helpful

It is meant to be both human-readable and machine-checkable by the validator.

## Security model

`key_facts.md` is for **non-secret** reference material only.

Safe examples:

- service-account email addresses
- public URLs
- project IDs, regions, and port numbers
- secret locations such as `.env`, Vault, or Secret Manager names

Never store:

- passwords
- API keys or tokens
- private keys or certificate material
- connection strings that contain credentials
- shell placeholders that effectively reveal how a secret is composed in a tracked file

If you can authenticate with it directly, it probably does not belong in project memory.

## Authoring notes

This package intentionally treats a few things as first-class quality work rather than afterthoughts:

- frontmatter that matches the Agent Skills specification
- a concise, trigger-friendly `description`
- progressive disclosure instead of a monolithic `SKILL.md`
- explicit validation and starter eval fixtures
- non-interactive scripts with predictable output for agent use
- a high-signal orientation layer for large repositories without bloating the core memory model

## License

MIT
