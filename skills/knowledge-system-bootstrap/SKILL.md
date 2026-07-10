---
name: knowledge-system-bootstrap
description: Bootstrap or migrate a repository to a compile-first Markdown knowledge system with durable project context, raw-source manifests, provenance and staleness checks, CI validation, and configuration for Claude Code, Codex, Cursor, and Windsurf. Use when a user wants repo-local project memory, wiki-first agent rules, repeatable raw-document intake, or this knowledge workflow replicated into another repository. Do not use for throwaway projects or when the user only wants a conventional documentation page.
---

# Knowledge System Bootstrap

Create a small, inspectable knowledge layer that survives agent sessions. Keep raw source files
local, compile reviewed conclusions into Markdown, and treat code as an implementation of the
documented intent.

## Workflow

1. Identify the target repository and a human-readable project name.
2. Inspect existing `AGENTS.md`, `CLAUDE.md`, wiki, manifest, and documentation files. Preserve
   user customizations.
3. Preview the scaffold:

   ```bash
   python scripts/bootstrap_knowledge_system.py /path/to/repo "Project Name" --dry-run
   ```

4. Run the same command without `--dry-run`. Existing files are skipped. Use `--force` only when
   the user explicitly wants generated files replaced; backups are created by default.
5. If raw documents are in scope, initialize and ingest them:

   ```bash
   python scripts/init_raw_root.py
   python scripts/ingest_raw.py
   ```

6. Validate the result:

   ```bash
   python scripts/wiki_check.py
   python scripts/raw_manifest_check.py
   python scripts/wiki_size_report.py
   ```

7. Run `stale_report.py` when raw sources exist. Use
   `delta_compile.py --write-drafts` to create reviewable recompilation drafts; never silently
   replace trusted wiki content.
8. Merge generated agent rules with existing rules when bootstrap skipped customized config
   files.

## Generated system

The renderer creates 33 files:

- eight pages under `docs/wiki/`, including schema and runtime guidance;
- `manifests/raw_sources.csv` and its schema metadata;
- deterministic Python tools for validation, intake, provenance, staleness, delta drafts, size
  reporting, raw-root setup, and memory export;
- platform instructions for Claude Code, Codex, Cursor, and Windsurf;
- three Claude commands, an upgrade helper, and a CI workflow.

Keep PDFs, spreadsheets, screenshots, archives, customer attachments, and other raw files out of
Git unless the user has deliberately approved publishing them. The manifest may be versioned;
review compiled wiki content for secrets and private information before committing it.

## Migration and maintenance

- Move existing durable project documentation into `docs/wiki/` deliberately; do not bulk-move
  files without understanding their role.
- Register local raw files through `ingest_raw.py` instead of hand-authoring large manifest
  batches.
- Prefer direct wiki reads while they remain effective. Treat `wiki_size_report.py` thresholds as
  heuristics and add search or RAG only when project measurements justify it.
- Upgrade generated scripts from a continuation-repository clone with:

  ```bash
  python scripts/upgrade_knowledge_system.py /path/to/bootstrapped-project
  ```

  The upgrader must not replace wiki content, manifests, or customized platform instructions.

## Bundled resources

- Run `scripts/bootstrap_knowledge_system.py` to render the scaffold.
- Read `references/playbook.md` only when the user needs the rationale, provenance model, or
  Git/raw split explained in depth.
