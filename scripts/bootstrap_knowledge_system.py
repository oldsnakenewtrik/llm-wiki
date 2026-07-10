"""
Convenience entry point — ALWAYS use this one.

The real implementation lives at:
  skills/knowledge-system-bootstrap/scripts/bootstrap_knowledge_system.py

This wrapper exists so the documented command works after cloning:
  python3 scripts/bootstrap_knowledge_system.py /path/to/project "Name"

DO NOT call the skill script directly unless you know why.
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

REAL_SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "knowledge-system-bootstrap" / "scripts" / "bootstrap_knowledge_system.py"

if not REAL_SCRIPT.exists():
    print(f"Error: cannot find {REAL_SCRIPT}", file=sys.stderr)
    print("Make sure you cloned the full LLM-wiki repo.", file=sys.stderr)
    sys.exit(1)

# ``os.execv`` loses argument boundaries on some Windows/Python combinations
# when either the interpreter or repository path contains spaces.  Execute the
# renderer as ``__main__`` in this interpreter instead; this preserves the CLI
# contract and propagates its SystemExit status unchanged on every platform.
sys.argv = [str(REAL_SCRIPT), *sys.argv[1:]]
runpy.run_path(str(REAL_SCRIPT), run_name="__main__")
