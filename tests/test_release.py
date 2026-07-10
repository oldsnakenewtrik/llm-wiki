"""Release metadata and continuation-link consistency checks."""
from __future__ import annotations

import json
import runpy
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VERSION = "1.4.0"
CONTINUATION = "oldsnakenewtrik/llm-wiki"


def test_generated_script_versions_are_current() -> None:
    templates = REPO / "skills" / "knowledge-system-bootstrap" / "templates" / "scripts"
    versioned = list(templates.glob("*.py")) + [templates / "upgrade.sh"]
    markers: dict[str, str] = {}
    for path in versioned:
        match = re.search(r"# llm-wiki-version:\s*(\S+)", path.read_text(encoding="utf-8"))
        if match:
            markers[path.name] = match.group(1)
    assert markers, "expected generated scripts with version markers"
    assert set(markers.values()) == {VERSION}, markers


def test_renderer_and_plugin_versions_match() -> None:
    renderer = (
        REPO
        / "skills"
        / "knowledge-system-bootstrap"
        / "scripts"
        / "bootstrap_knowledge_system.py"
    ).read_text(encoding="utf-8")
    assert f'__version__ = "{VERSION}"' in renderer

    plugin = json.loads((REPO / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads(
        (REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    assert plugin["version"] == VERSION
    assert market["metadata"]["version"] == VERSION
    assert market["plugins"][0]["version"] == VERSION


def test_active_distribution_files_use_continuation_repo() -> None:
    active = [
        REPO / "README.md",
        REPO / "UNIVERSAL.md",
        REPO / "CONTRIBUTING.md",
        REPO / "SECURITY.md",
        REPO / "scripts" / "install-codex-skill.sh",
        REPO / "scripts" / "upgrade_knowledge_system.py",
        REPO / "scripts" / "version_check.py",
        REPO / "skills" / "knowledge-system-bootstrap" / "templates" / "scripts" / "upgrade.sh",
        REPO / "skills" / "knowledge-system-bootstrap" / "templates" / "scripts" / "version_check.py",
    ]
    for path in active:
        text = path.read_text(encoding="utf-8")
        assert CONTINUATION in text, f"missing continuation endpoint in {path.relative_to(REPO)}"


def test_recovery_record_and_original_notice_are_present() -> None:
    provenance = (REPO / "PROVENANCE.md").read_text(encoding="utf-8")
    license_text = (REPO / "LICENSE").read_text(encoding="utf-8")
    assert "2938022db022c0722a7b2bfd1ba2ca090158df4a" in provenance
    assert "Copyright (c) 2026 Ss1024sS" in license_text


def test_version_check_does_not_offer_downgrades() -> None:
    namespace = runpy.run_path(str(REPO / "scripts" / "version_check.py"), run_name="release_test")
    parse_version = namespace["parse_version"]
    assert parse_version("1.4.0") > parse_version("1.3.0")
    assert not parse_version("1.3.0") > parse_version("1.4.0")
