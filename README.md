# LLM Wiki

Turn a project repository into durable, agent-readable memory using ordinary Markdown.

This is a community-maintained continuation of the original MIT-licensed
`Ss1024sS/LLM-wiki` project. The original repository disappeared in 2026; its complete final
commit and history were recovered, retained, and are documented in
[PROVENANCE.md](./PROVENANCE.md). The original author remains credited in the license and Git
history.

## The pattern

```text
raw sources (local, immutable, usually outside Git)
        |
        |  an AI agent compiles and reconciles
        v
wiki pages (Markdown consensus, reviewed and versioned)
        |
        |  an AI agent uses the current project knowledge
        v
code and other deliverables
```

The practical rules are simple:

1. Compile durable conclusions into wiki pages instead of leaving them in chat.
2. Write decisions and changed project state back during the same session.
3. Start with direct Markdown reads; add retrieval infrastructure only when measurement shows
   you need it.
4. Keep the storage portable: filesystem + Markdown. Obsidian is optional.
5. Treat code as an implementation of documented intent, not the only record of that intent.

The size thresholds reported by `wiki_size_report.py` are planning heuristics, not performance
guarantees.

## What it installs

The bootstrapper creates 33 files without third-party Python dependencies:

- eight starter pages in `docs/wiki/`, with schema and runtime guidance;
- a versioned raw-source manifest (the raw documents themselves stay local);
- ingest, provenance, staleness, delta-draft, size, and validation scripts;
- `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, and `.windsurfrules`;
- Claude Code commands and a GitHub Actions lint workflow.

It skips existing files by default. `--force` overwrites them only after making timestamped
backups, unless `--no-backup` is explicitly supplied.

## Quick start

### Ask an agent

Give a filesystem-capable coding agent this instruction:

```text
Read https://github.com/oldsnakenewtrik/llm-wiki/blob/main/UNIVERSAL.md and set up the knowledge system for this project.
```

### Run the bootstrapper

```bash
git clone https://github.com/oldsnakenewtrik/llm-wiki.git
cd llm-wiki

# Preview; writes nothing.
python scripts/bootstrap_knowledge_system.py /path/to/project "My Project" --dry-run

# Create the files.
python scripts/bootstrap_knowledge_system.py /path/to/project "My Project"
```

`python3` works too. The root wrapper is supported on Linux, macOS, and Windows, including paths
with spaces.

Then, from the bootstrapped project:

```bash
python scripts/init_raw_root.py
python scripts/wiki_check.py
python scripts/raw_manifest_check.py
python scripts/wiki_size_report.py
```

## Agent integrations

| Platform | Integration |
| --- | --- |
| Claude Code | Plugin plus generated `CLAUDE.md` |
| Codex | Installable skill plus generated `AGENTS.md` |
| Cursor | Generated `.cursorrules` |
| Windsurf | Generated `.windsurfrules` |
| Other agents | Follow [UNIVERSAL.md](./UNIVERSAL.md) |

Claude Code plugin:

```text
claude plugin install oldsnakenewtrik/llm-wiki
```

Codex skill:

```text
Use $skill-installer to install https://github.com/oldsnakenewtrik/llm-wiki/tree/main/skills/knowledge-system-bootstrap
```

The shell helper remains available as `bash scripts/install-codex-skill.sh`.

## Daily workflow

At session start, the agent reads `index.md`, `current-status.md`, and recent `log.md` entries.
During work, it opens only relevant pages. Before finishing, it writes durable decisions and
current state back to the wiki.

When source documents change:

```bash
python scripts/ingest_raw.py
python scripts/stale_report.py
python scripts/delta_compile.py --write-drafts
```

The delta step creates reviewable drafts; it does not silently rewrite trusted wiki pages.

Keep confidential PDFs, spreadsheets, archives, and customer files out of the public Git
repository. Commit the manifest and compiled, reviewed knowledge only when that content is safe
to publish.

## Upgrading an existing project

On Linux/macOS (or Git Bash):

```bash
cd /path/to/project
bash scripts/upgrade.sh
```

On any platform, from this repository clone:

```bash
python scripts/upgrade_knowledge_system.py /path/to/project
```

Upgrades replace generated utility scripts and CI only. They do not overwrite wiki content,
manifests, or customized agent configuration files.

## Verify it

```bash
pytest -q
```

The suite bootstraps isolated projects and exercises structure validation, raw manifests,
frontmatter, links, provenance behavior, backups, dry runs, plugin metadata, and the Windows
wrapper regression.

## Documentation

- [Universal setup guide](./UNIVERSAL.md)
- [Knowledge-system playbook](./docs/knowledge-system-playbook.md)
- [Raw intake and stale detection](./docs/ingest-pipeline.md)
- [Example project](./examples/demo-project/)
- [Recovery and authorship record](./PROVENANCE.md)

## License and credit

MIT. Retain the copyright and permission notice when redistributing substantial portions.

The LLM Wiki pattern is credited to
[Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
The original implementation and engineering practice are credited to
[Ss1024sS](https://github.com/Ss1024sS). This continuation is maintained by
[@oldsnakenewtrik](https://github.com/oldsnakenewtrik) and contributors.
