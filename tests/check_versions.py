#!/usr/bin/env python3
"""
Two separate checks, because they catch two different failures and the first one alone
does NOT catch the second. Saying so precisely matters: an earlier draft of this file
claimed the agreement check prevented "a commit shipped content and left the version
behind", and both of the commits it named pass it cleanly.

  A. AGREEMENT (always runs). The version is recorded in four places and nothing was
     checking that they match each other:
       1. .claude-plugin/marketplace.json          -> plugins[0].version
       2. plugins/show-and-tell/.claude-plugin/plugin.json -> version
       3. SKILL.md frontmatter                     -> version:
       4. README.md "Version History"              -> a `- **v<version>** (` line
     (The plugin copy of SKILL.md is a synced duplicate, not a fifth place — sync-plugin.sh
     and the CI sync check own that one.)

  B. WAS IT BUMPED AT ALL (needs --against <ref>). Four places can agree perfectly and all
     be stale together: content ships, the version is untouched, everything is internally
     consistent and A is green. This compares against a base ref and fails if SKILL.md /
     assets / scripts / references changed while plugin.json's version did not.

     Checked against the two commits in this repo's history that shipped without a bump:
     345b4c7 changed SKILL.md at version 2.1.0 and B now FAILS it. f8d6f39 touched only
     README.md and the banner images, which this definition of "shipped content" does not
     cover, so B still passes it — deliberately, because a README typo is not a release.
     If you want the changelog and the README gated too, widen SHIPPED; do not assume
     they already are.

Exit codes: 0 = checked and clean · 1 = a problem · 3 = check B could not run (no git, no
such ref). 3 is NOT a pass — if you asked for B and got 3, B did not happen.

This lives in tests/, which sync-plugin.sh does NOT copy into the plugin: it is a repo
gate, not part of the shipped skill.

Run: python3 tests/check_versions.py [--against origin/main]
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Changing any of these is "shipping content" and earns a version bump.
SHIPPED = ("SKILL.md", "assets/", "scripts/", "references/")


def frontmatter_version(text):
    fm = re.search(r"\A---\n(.*?)\n---", text, re.S)
    if not fm:
        return None, "SKILL.md has no frontmatter block"
    hits = re.findall(r"^version:\s*(\S+)", fm.group(1), re.M)
    if not hits:
        return None, "SKILL.md frontmatter has no `version:` field"
    if len(hits) > 1:
        # YAML resolves duplicate keys last-wins; a first-match read would disagree with
        # every other tool. Refuse rather than pick one.
        return None, f"SKILL.md frontmatter has {len(hits)} `version:` lines: {hits}"
    return hits[0], None


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True, check=True).stdout


def check_agreement():
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    plugin = json.loads((ROOT / "plugins/show-and-tell/.claude-plugin/plugin.json").read_text())
    readme = (ROOT / "README.md").read_text()
    fm, err = frontmatter_version((ROOT / "SKILL.md").read_text())

    canonical = plugin["version"]
    problems = []
    if err:
        problems.append(err)

    found = {"plugin.json": canonical,
             "marketplace.json": marketplace["plugins"][0]["version"],
             "SKILL.md frontmatter": fm}
    print(f"A. agreement — plugin.json is the canon at {canonical}")
    for where, v in found.items():
        ok = v == canonical
        print(f"   {'✓' if ok else '✗'} {where}: {v}")
        if not ok:
            problems.append(f"{where} says {v}, plugin.json says {canonical}")

    # Anchor to the Version History heading so a `- **v…** (` line elsewhere can't satisfy it.
    history = readme.split("Version History", 1)
    entry_ok = len(history) > 1 and f"- **v{canonical}** (" in history[1]
    print(f"   {'✓' if entry_ok else '✗'} README.md Version History entry for v{canonical}")
    if not entry_ok:
        problems.append(f"README.md's Version History has no `- **v{canonical}** (…)` entry")
    return problems, canonical


def check_bumped(base, canonical):
    """Did this branch ship content without moving the version? Returns (problems, ran)."""
    try:
        merge_base = git("merge-base", base, "HEAD").strip()
        changed = git("diff", "--name-only", f"{merge_base}..HEAD").split()
        was = json.loads(git("show", f"{merge_base}:plugins/show-and-tell/.claude-plugin/plugin.json"))["version"]
    except (subprocess.CalledProcessError, FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"B. bumped — UNCHECKED against {base}: {type(e).__name__}. This is not a pass.")
        return [], False

    shipped = [f for f in changed if f.startswith(SHIPPED)]
    print(f"B. bumped — {len(shipped)} shipped file(s) changed since {base} ({merge_base[:8]}); "
          f"version {was} -> {canonical}")
    if shipped and was == canonical:
        for f in shipped[:8]:
            print(f"   changed: {f}")
        return [f"{len(shipped)} shipped file(s) changed but plugin.json's version is still "
                f"{was} — bump it, and add the README entry"], True
    print("   ✓" if shipped else "   ✓ no shipped files changed")
    return [], True


def main():
    against = None
    if "--against" in sys.argv:
        against = sys.argv[sys.argv.index("--against") + 1]

    problems, canonical = check_agreement()
    ran_b = True
    if against:
        more, ran_b = check_bumped(against, canonical)
        problems += more

    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  ✗", p)
        return 1
    if against and not ran_b:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
