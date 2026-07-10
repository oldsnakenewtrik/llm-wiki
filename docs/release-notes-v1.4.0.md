# v1.4.0 — Community continuation and Windows support

This release restores a maintained home for the original MIT-licensed project and fixes the most
visible portability problem found during recovery.

## Windows bootstrap fix

The public wrapper previously delegated with `os.execv`. On affected Windows/Python combinations,
paths containing spaces lost their argument boundaries, so the renderer never ran. The wrapper
now executes the internal renderer with `runpy`, preserving arguments and exit status on Windows,
Linux, and macOS.

The existing tests already create projects below a user temp path. They now pass on Windows, and
CI runs the pytest suite across all three operating-system families.

The upgrader also escapes unsupported characters when a legacy Windows code page cannot display
generated template text, instead of crashing after files have already been updated.

## Maintained endpoints

Active install, release-check, upgrade, security, plugin, and documentation links now target
`oldsnakenewtrik/llm-wiki`. Historical notes still identify the original repository where that
context matters.

## Provenance

The original final commit and all 40 upstream commits remain in history. See
[PROVENANCE.md](../PROVENANCE.md) for the commit identifier, recovery route, license, and the
boundary between original and continuation work.

## Compatibility

- Python: standard library at runtime; pytest is needed only for repository tests.
- Bootstrap output: still 33 files.
- Manifest schema: unchanged at version 1.
- Existing projects: generated scripts and CI can be upgraded without replacing wiki pages,
  manifests, or customized agent instructions.
