#!/usr/bin/env python3
"""Fail the build when the repository's duplicated metadata drifts apart.

Plugin metadata is restated in three hand-written files, and each skill states
its version in both SKILL.md and metadata.json. Nothing regenerates any of
them, so this script is the only thing keeping them honest.

Checks performed:

1. Root plugin.json satisfies the Agent Plugins 1.0.0 manifest rules.
2. plugin.json, .claude-plugin/plugin.json, and the .claude-plugin/marketplace.json
   entry agree on every field they share.
3. Each skill's SKILL.md frontmatter agrees with its metadata.json.
4. Each skill's version badge in README.md matches that skill's version.
5. Every relative link in README.md points at a file that exists.

Skill versions are deliberately NOT required to equal the plugin version: a
plugin release can bundle unchanged skills.

Stdlib only, so CI needs no dependency install step.

Usage: python3 .github/scripts/check-consistency.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# Mirrors https://agent-plugins.org/schemas/1.0.0/plugin.schema.json. Inlined
# rather than fetched: CI must not depend on the network to validate a manifest.
SCHEMA_ID = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MANIFEST_FIELDS = {
    "$schema", "name", "version", "description", "author",
    "homepage", "repository", "license", "keywords", "extensions",
}
MANIFEST_REQUIRED = ("$schema", "name")
NAME_PATTERN = re.compile(r"(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?")
AUTHOR_FIELDS = {"name", "email", "url"}

# Fields the three manifests must state identically.
SHARED_FIELDS = ("name", "version", "description", "author", "homepage", "license", "keywords")

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def load_json(relative: str):
    path = REPO / relative
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"{relative}: missing")
    except json.JSONDecodeError as exc:
        fail(f"{relative}: invalid JSON — {exc}")
    return None


def parse_frontmatter(path: Path) -> dict[str, str]:
    """Read the flat and one-level-nested keys out of a SKILL.md frontmatter block.

    Nested keys are returned dotted, so `metadata.version` reads as
    "metadata.version". Deliberately not a YAML parser — the frontmatter these
    skills use is a fixed, simple shape, and this keeps the script dependency-free.
    """
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        fail(f"{path.relative_to(REPO)}: no YAML frontmatter block")
        return {}

    fields: dict[str, str] = {}
    parent = None
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        entry = re.match(r"^(\s*)([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not entry:
            continue
        indent, key, value = entry.group(1), entry.group(2), entry.group(3).strip()
        value = value[1:-1] if len(value) >= 2 and value[0] == value[-1] in "\"'" else value
        if not indent:
            parent = key if not value else None
            if value:
                fields[key] = value
        elif parent:
            fields[f"{parent}.{key}"] = value
    return fields


def check_manifest_schema(manifest) -> None:
    """Check 1: root plugin.json against the Agent Plugins 1.0.0 manifest rules."""
    if manifest is None:
        return

    for field in MANIFEST_REQUIRED:
        if field not in manifest:
            fail(f"plugin.json: missing required field '{field}' (spec 1.0.0 §5.3)")

    for field in sorted(set(manifest) - MANIFEST_FIELDS):
        fail(f"plugin.json: '{field}' is not a permitted top-level field (spec 1.0.0 §5.2)")

    if manifest.get("$schema") != SCHEMA_ID:
        fail(f"plugin.json: $schema must be exactly {SCHEMA_ID} (spec 1.0.0 §5.2)")

    name = manifest.get("name")
    if isinstance(name, str) and not (1 <= len(name) <= 64 and NAME_PATTERN.fullmatch(name)):
        fail(f"plugin.json: name '{name}' violates the naming constraints (spec 1.0.0 §5.5)")

    author = manifest.get("author")
    if isinstance(author, dict):
        for field in sorted(set(author) - AUTHOR_FIELDS):
            fail(f"plugin.json: author.{field} is not a permitted field (spec 1.0.0 §5.4)")


def check_manifests_agree(manifest, claude_manifest, marketplace) -> None:
    """Check 2: the three hand-written copies of the plugin metadata."""
    if manifest is None or claude_manifest is None or marketplace is None:
        return

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail(".claude-plugin/marketplace.json: expected a non-empty 'plugins' array")
        return

    name = manifest.get("name")
    entry = next((p for p in plugins if p.get("name") == name), None)
    if entry is None:
        fail(f".claude-plugin/marketplace.json: no plugins[] entry named '{name}'")
        return

    sources = {
        ".claude-plugin/plugin.json": claude_manifest,
        ".claude-plugin/marketplace.json plugins[]": entry,
    }
    for label, other in sources.items():
        for field in SHARED_FIELDS:
            expected, actual = manifest.get(field), other.get(field)
            if actual != expected:
                fail(f"{label}: {field} is {actual!r}, but plugin.json says {expected!r}")

    if claude_manifest.get("repository") != manifest.get("repository"):
        fail(
            f".claude-plugin/plugin.json: repository is {claude_manifest.get('repository')!r}, "
            f"but plugin.json says {manifest.get('repository')!r}"
        )


def check_skills() -> dict[str, str]:
    """Check 3: SKILL.md frontmatter against metadata.json. Returns skill -> version."""
    versions: dict[str, str] = {}
    skills_dir = REPO / "skills"
    if not skills_dir.is_dir():
        fail("skills/: missing or not a directory (spec 1.0.0 §6.1)")
        return versions

    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            fail(f"skills/{skill}/: no SKILL.md, so no client will discover it (spec 1.0.0 §7.1)")
            continue

        frontmatter = parse_frontmatter(skill_md)
        if frontmatter.get("name") != skill:
            fail(
                f"skills/{skill}/SKILL.md: frontmatter name is "
                f"{frontmatter.get('name')!r}, but the directory is {skill!r}"
            )
        if not frontmatter.get("description"):
            fail(f"skills/{skill}/SKILL.md: frontmatter is missing a description")

        metadata = load_json(f"skills/{skill}/metadata.json")
        if metadata is None:
            continue

        declared = frontmatter.get("metadata.version")
        recorded = metadata.get("version")
        if declared != recorded:
            fail(
                f"skills/{skill}: SKILL.md says version {declared!r}, "
                f"but metadata.json says {recorded!r}"
            )
        if recorded:
            versions[skill] = recorded
    return versions


def check_readme(skill_versions: dict[str, str]) -> None:
    """Checks 4 and 5: README version badges and relative links."""
    readme = REPO / "README.md"
    if not readme.is_file():
        fail("README.md: missing")
        return
    text = readme.read_text(encoding="utf-8")

    for skill, version in skill_versions.items():
        heading = next((l for l in text.splitlines() if l.startswith(f"### {skill}")), None)
        if heading is None:
            fail(f"README.md: no '### {skill}' section for the skill in skills/{skill}/")
        elif f"v{version}" not in heading:
            fail(f"README.md: the '{skill}' badge does not show v{version}")

    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        if not (REPO / target.split("#", 1)[0]).exists():
            fail(f"README.md: link target '{target}' does not exist")


def main() -> int:
    manifest = load_json("plugin.json")
    claude_manifest = load_json(".claude-plugin/plugin.json")
    marketplace = load_json(".claude-plugin/marketplace.json")

    check_manifest_schema(manifest)
    check_manifests_agree(manifest, claude_manifest, marketplace)
    check_readme(check_skills())

    if failures:
        print(f"Consistency check failed with {len(failures)} problem(s):\n", file=sys.stderr)
        for problem in failures:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    version = manifest.get("version") if manifest else "?"
    print(f"Consistency check passed: gradle-skills {version} is internally consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
