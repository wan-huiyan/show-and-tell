#!/usr/bin/env python3
"""
The version is recorded in four places and nothing was checking that they agree.
Twice in this repo's history a commit shipped content and left the version behind.

  1. .claude-plugin/marketplace.json  -> plugins[0].version
  2. plugins/show-and-tell/.claude-plugin/plugin.json -> version
  3. SKILL.md frontmatter -> version:
  4. README.md "Version History" -> a `- **v<version>** (` line

(The plugin copy of SKILL.md is a synced duplicate, not a fifth place — sync-plugin.sh
and the CI sync check own that one.)

This lives in tests/, which sync-plugin.sh does NOT copy into the plugin: it is a repo
gate, not part of the shipped skill.

Run: python3 tests/check_versions.py     Exit 0 = agree, 1 = disagree.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    plugin = json.loads((ROOT / "plugins/show-and-tell/.claude-plugin/plugin.json").read_text())
    skill = (ROOT / "SKILL.md").read_text()
    readme = (ROOT / "README.md").read_text()

    fm = re.search(r"\A---\n(.*?)\n---", skill, re.S)
    if not fm:
        print("✗ SKILL.md has no frontmatter block"); return 1
    m = re.search(r"^version:\s*(\S+)", fm.group(1), re.M)
    if not m:
        print("✗ SKILL.md frontmatter has no `version:` field"); return 1

    canonical = plugin["version"]
    found = {
        "plugin.json": canonical,
        "marketplace.json": marketplace["plugins"][0]["version"],
        "SKILL.md frontmatter": m.group(1),
    }
    problems = [f"{where} says {v}, plugin.json says {canonical}"
                for where, v in found.items() if v != canonical]

    if f"- **v{canonical}** (" not in readme:
        problems.append(
            f"README.md Version History has no `- **v{canonical}** (…)` entry — "
            "bump the changelog too, it is the place that goes stale")

    print(f"check_versions: plugin.json is the canon at {canonical}")
    for where, v in found.items():
        print(f"  {'✓' if v == canonical else '✗'} {where}: {v}")
    print(f"  {'✓' if not any('README' in p for p in problems) else '✗'} README.md Version History entry")
    if problems:
        print("  PROBLEMS:")
        for p in problems:
            print("   ✗", p)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
