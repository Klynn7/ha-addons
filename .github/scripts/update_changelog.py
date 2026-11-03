#!/usr/bin/env python3
"""Prepend a release entry to an add-on CHANGELOG.md.

Usage: update_changelog.py CHANGELOG OLD_MANIFEST NEW_MANIFEST VERSION [COMMITS_FILE]

Entry contents, in order:
  1. Notes from an "## Unreleased" section, if one exists (it is consumed).
     Otherwise, subjects of commits that changed the add-on since the last
     release (COMMITS_FILE, one per line), if any.
  2. Debian package changes between the two build manifests.
  3. A fallback line if nothing else changed (e.g. a forced rebuild).
"""
import re
import sys
from pathlib import Path

HEADER = "# Changelog"


def read_manifest(path: Path) -> tuple[str | None, dict[str, str]]:
    src_hash, pkgs = None, {}
    if not path.exists():
        return src_hash, pkgs
    for line in path.read_text().splitlines():
        if line.startswith("# source-sha256 "):
            src_hash = line.split()[-1]
        elif line.strip() and not line.startswith("#"):
            name, _, version = line.partition(" ")
            pkgs[name] = version
    return src_hash, pkgs


def package_lines(old: dict[str, str], new: dict[str, str]) -> list[str]:
    lines = []
    for name in sorted(old.keys() | new.keys()):
        before, after = old.get(name), new.get(name)
        if before == after:
            continue
        if before is None:
            lines.append(f"- Added `{name}` {after}")
        elif after is None:
            lines.append(f"- Removed `{name}` (was {before})")
        else:
            lines.append(f"- `{name}` {before} → {after}")
    return lines


def split_unreleased(body: str) -> tuple[str, list[str]]:
    """Return (body without the Unreleased section, its bullet lines)."""
    m = re.search(r"^## Unreleased[^\n]*\n(.*?)(?=^## |\Z)", body, re.M | re.S)
    if not m:
        return body, []
    notes = [l for l in m.group(1).strip().splitlines() if l.strip()]
    return body[: m.start()] + body[m.end():], notes


def main() -> None:
    changelog, old_manifest, new_manifest, version = map(Path, sys.argv[1:5])
    version = str(version)
    commits_file = Path(sys.argv[5]) if len(sys.argv) > 5 else None

    old_hash, old_pkgs = read_manifest(old_manifest)
    new_hash, new_pkgs = read_manifest(new_manifest)

    text = changelog.read_text() if changelog.exists() else f"{HEADER}\n"
    if text.startswith(HEADER):
        text = text[len(HEADER):]
    text, notes = split_unreleased(text.lstrip("\n"))

    if not notes and old_hash != new_hash and commits_file and commits_file.exists():
        notes = [f"- {s.strip()}" for s in commits_file.read_text().splitlines() if s.strip()]
    if not notes and old_hash and old_hash != new_hash:
        notes = ["- Add-on configuration or scripts updated (see repository history)."]

    pkg = package_lines(old_pkgs, new_pkgs)

    entry = [f"## {version}", ""]
    if notes:
        entry += notes + [""]
    if pkg:
        entry += ["Debian package updates:", ""] + pkg + [""]
    if not notes and not pkg:
        entry += ["- Rebuild with no package or source changes.", ""]

    changelog.write_text(f"{HEADER}\n\n" + "\n".join(entry) + "\n" + text.rstrip("\n") + "\n")


if __name__ == "__main__":
    main()
