#!/usr/bin/env python3
"""
Render-safety check for a self-contained explainer HTML (no browser needed).
Catches the silent-failure cases that make a page open broken:
  1. Unbalanced tags (structure broke mid-edit).
  2. A `var(--x)` referenced but NOT defined in :root  -> that text/colour silently disappears
     (see skill css-var-undefined-silent-declaration-drop). This is the #1 "half the page is
     invisible" cause and a browser screenshot won't always make it obvious.

Usage:  python3 check_html.py <file.html> [--expect "phrase one" "phrase two" ...]
Exit 0 = clean; exit 1 = problems found (printed). The visual polish still wants a real `open`,
but this gate stops you handing the user a page with invisible text.
"""
import sys, re
from html.parser import HTMLParser

VOID = {"meta", "br", "img", "input", "hr", "link", "area", "base", "col", "embed",
        "param", "source", "track", "wbr"}

class Balance(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag in self.stack:
            # pop to the matching open tag (tolerate minor nesting slop)
            while self.stack and self.stack.pop() != tag:
                pass
        else:
            self.errors.append(f"stray </{tag}> with no open tag")

def main():
    if len(sys.argv) < 2:
        print("usage: check_html.py <file.html> [--expect phrase ...]"); sys.exit(2)
    path = sys.argv[1]
    expect = sys.argv[sys.argv.index("--expect") + 1:] if "--expect" in sys.argv else []
    html = open(path, encoding="utf-8").read()

    problems = []

    # 1) tag balance
    b = Balance(); b.feed(html)
    if b.stack:
        problems.append(f"unclosed tags: {b.stack[-8:]}")
    problems += b.errors

    # 2) CSS variables: every var(--x) used must be defined as `--x:` somewhere in a <style> block
    styles = " ".join(re.findall(r"<style>(.*?)</style>", html, re.S))
    defined = set(re.findall(r"(--[\w-]+)\s*:", styles))
    used = set(re.findall(r"var\((--[\w-]+)", html))
    missing = sorted(used - defined)
    if missing:
        problems.append(f"undefined CSS vars used (text/colour will silently vanish): {missing}")

    # 3) optional content presence (catch a template slot left unfilled / a placeholder shipped)
    for phrase in expect:
        if phrase not in html:
            problems.append(f"expected phrase NOT found: {phrase!r}")
    leftover = [m for m in re.findall(r"__[A-Z_]+__", html)]
    if leftover:
        problems.append(f"unfilled template placeholders remain: {sorted(set(leftover))}")

    print(f"check_html: {path}")
    print(f"  CSS vars defined={len(defined)} used={len(used)}")
    if problems:
        print("  PROBLEMS:")
        for p in problems:
            print("   ✗", p)
        sys.exit(1)
    print("  ✓ tags balanced · all CSS vars defined · no leftover placeholders")
    sys.exit(0)

if __name__ == "__main__":
    main()
