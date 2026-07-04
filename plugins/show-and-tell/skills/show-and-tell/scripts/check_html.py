#!/usr/bin/env python3
"""
Render-safety check for a self-contained explainer HTML (no browser needed).
Catches the silent-failure cases that make a page open broken:
  1. Unbalanced tags (structure broke mid-edit).
  2. A `var(--x)` referenced but NOT defined in :root  -> that text/colour silently disappears
     (see skill css-var-undefined-silent-declaration-drop). This is the #1 "half the page is
     invisible" cause and a browser screenshot won't always make it obvious.
  3. A theme block (paper/midnight) missing a token the base :root defines -> that element
     silently keeps the default theme's colour (e.g. near-white ink on the paper background).
  4. Render-time network references (external <img>/<script>/<link>/@import/url(http...)) ->
     breaks the "opens from file://, no network" promise. Plain <a href> links are fine.
  5. Illustrations without a text alternative (<img> missing alt, <svg> with no aria) and
     hardcoded colours in the body (fill="#..."), which won't follow the theme switcher.

HTML comments and CSS /* */ comments are stripped before analysis — a comment can't break a
render, and the template documents its rules in comments.

Usage:  python3 check_html.py <file.html> [--template] [--expect "phrase one" "phrase two" ...]
  --template  allow __PLACEHOLDER__ slots (for checking the shipped template itself, not a report)
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
    template_mode = "--template" in sys.argv
    expect = sys.argv[sys.argv.index("--expect") + 1:] if "--expect" in sys.argv else []
    raw = open(path, encoding="utf-8").read()
    # analysis copy: comments can't break a render, so drop them before checking
    html = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    html = re.sub(r"/\*.*?\*/", " ", html, flags=re.S)

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

    # 3) theme parity: each :root[data-theme="x"] block must re-declare every token the base
    #    :root defines, or that element silently keeps the default theme's colour in that theme.
    #    (The FIRST plain :root is the canon; later plain ones — e.g. inside @media print — are
    #    intentional partial overrides and are skipped.)
    base_vars, theme_blocks = None, {}
    for m in re.finditer(r':root(?:\[data-theme="([\w-]+)"\])?\s*\{([^}]*)\}', styles):
        name, body = m.group(1), m.group(2)
        if name is None:
            if base_vars is None:
                base_vars = set(re.findall(r"(--[\w-]+)\s*:", body))
        else:
            theme_blocks[name] = set(re.findall(r"(--[\w-]+)\s*:", body))
    if base_vars:
        for name, tvars in theme_blocks.items():
            gap = sorted(base_vars - tvars)
            if gap:
                problems.append(
                    f'theme "{name}" is missing overrides for {gap} — those elements will keep '
                    f"the default theme's colours (wrong contrast) when the reader switches")

    # 4) self-contained: nothing the RENDER fetches from the network. <a href> links are fine —
    #    the promise is that the page *displays* fully from file:// with no connection.
    for pat, what in [
        (r'<(?:img|script|iframe|video|audio|source|embed)\b[^>]*\bsrc=["\']https?://', "external src="),
        (r'<link\b[^>]*\bhref=["\']https?://', "external <link href>"),
        (r'@import\b', "CSS @import"),
        (r'url\(\s*["\']?https?://', "css url(http…)"),
    ]:
        if re.search(pat, html, re.I):
            problems.append(f"not self-contained — render-time network reference found: {what}")

    # 5a) illustrations need a text alternative
    for m in re.finditer(r"<img\b[^>]*>", html, re.I):
        if not re.search(r"\balt\s*=", m.group(0)):
            problems.append(f"<img> without alt text: {m.group(0)[:70]}")
    for m in re.finditer(r"<svg\b[^>]*>", html, re.I):
        tag = m.group(0)
        before = html[max(0, m.start() - 300):m.start()]
        if not re.search(r"aria-(label|labelledby|hidden)|\brole\s*=", tag) and \
           not re.search(r'aria-label\s*=', before):
            problems.append(
                "inline <svg> with no text alternative — add aria-label, wrap it in "
                '<figure role="img" aria-label="…">, or mark it aria-hidden="true" if decorative')

    # 5b) hardcoded colours in the body break the 🎮/📄/🌌 theme switcher (and print)
    body_html = re.sub(r"<style>.*?</style>", "", html, flags=re.S)
    hard = set(re.findall(r'(?:fill|stroke|stop-color)\s*=\s*["\']\s*(#[0-9a-fA-F]{3,8})\b', body_html))
    hard |= set(re.findall(r'style\s*=\s*["\'][^"\']*(?:color|background[^:;"\']*|fill|stroke)\s*:\s*(#[0-9a-fA-F]{3,8})\b', body_html))
    if hard:
        problems.append(f"hardcoded colours outside the theme system (use var(--x) instead): {sorted(hard)}")

    # 6) optional content presence (catch a template slot left unfilled / a placeholder shipped)
    for phrase in expect:
        if phrase not in raw:
            problems.append(f"expected phrase NOT found: {phrase!r}")
    leftover = [] if template_mode else re.findall(r"__[A-Z][A-Z0-9_]*__", html)
    if leftover:
        problems.append(f"unfilled template placeholders remain: {sorted(set(leftover))}")

    print(f"check_html: {path}")
    print(f"  CSS vars defined={len(defined)} used={len(used)} · themes checked={sorted(theme_blocks)}")
    if problems:
        print("  PROBLEMS:")
        for p in problems:
            print("   ✗", p)
        sys.exit(1)
    print("  ✓ tags balanced · all CSS vars defined · themes in parity · self-contained ·"
          " figures labelled · no hardcoded colours · no leftover placeholders")
    sys.exit(0)

if __name__ == "__main__":
    main()
