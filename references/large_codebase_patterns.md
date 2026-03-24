# Large Codebase Patterns

Use this guidance when project memory needs to help a fresh session orient quickly on a large, long-lived, or multi-component repository.

## When to add `architecture.md`

Add `docs/project_notes/architecture.md` when one or more of these are true:

- a fresh session often needs a system map before it can safely explore the codebase
- the repository has multiple services, packages, apps, or deployment surfaces
- the same architectural misunderstandings or sharp edges keep recurring across sessions
- `bugs.md`, `decisions.md`, and `issues.md` are useful but too scattered to serve as a fast-start overview

Do not create `architecture.md` just to duplicate the README. Use it for the context that future sessions repeatedly need and repeatedly forget.

## Recommended read order for a fresh session

For large repos, prefer this order:

1. `architecture.md` if present
2. `decisions.md` for constraints and superseded choices
3. `key_facts.md` for non-secret environment and platform facts
4. topic-relevant entries in `bugs.md`
5. recent entries in `issues.md` when handoff or current work matters
6. repository exploration only after memory narrows what to inspect

If the task is narrow, use `scripts/search_project_memory.py` first instead of reading every memory file.

## What belongs in `architecture.md`

Good candidates:

- component boundaries and responsibilities
- key entry points or directories to inspect first
- critical flows such as auth, background jobs, migrations, or data pipelines
- durable gotchas and prior misunderstandings
- change hazards where coupling is easy to underestimate

Poor candidates:

- sprint notes
- transient rollout minutiae
- secrets or credential-bearing connection details
- exhaustive code walkthroughs that are better discovered from the code itself

## Monorepo pattern

For monorepos, prefer one root `architecture.md` first.

- Start with a top-level component map and only split into service-local memory when the root file becomes hard to scan.
- Cross-link to service-local docs or runbooks instead of copying them wholesale.
- Keep shared ADRs in `decisions.md`; use `architecture.md` to explain where they matter.

## Capturing prior misunderstandings

When a misunderstanding keeps wasting time across sessions:

- put the recurring failure in `bugs.md` if it behaves like a bug or sharp edge
- put the durable “how this part of the system really works” note in `architecture.md`
- put the durable choice in `decisions.md` if the fix reflects a lasting decision

A good test is: what would you want a fresh session to read in the first minute? That belongs in `architecture.md` or should be cross-linked from it.

## Keep memory high-signal

Large repositories need memory that is easier to skim than the codebase itself.

- Prefer short bullets over long prose.
- Keep section titles concrete and reusable.
- Push ephemeral task detail into `issues.md` and preserve only the durable lesson elsewhere.
- Mark deprecated guidance clearly so future sessions do not inherit stale context.
