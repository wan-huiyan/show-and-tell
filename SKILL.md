---
name: show-and-tell
description: >
  Turn dense technical findings, an analysis, a code/research session outcome, or a jargon-heavy
  document into a genuinely PLAIN-ENGLISH self-contained HTML explainer a non-technical or busy
  stakeholder can actually understand AND trust — built on a single everyday metaphor carried through
  the whole piece (the bad news included), with the REAL numbers shown honestly beside each plain
  claim, an "engineer's note" layer so technical readers aren't shortchanged, a foregrounded
  honesty/limits box, and a bundled FACT-VERIFIER that checks every claim, number, and metaphor back
  against the source document to catch translation drift before anyone reads it (self-contained, opens
  straight from file:// — no build, no server; arcade/pixel aesthetic). Use this WHENEVER the
  user wants to explain technical work in plain English, make a pretty/shareable report, one-pager, or
  recap, summarize an investigation/session "so my boss/team/client can understand it," translate
  jargon results for a lay audience, or asks for an explainer/writeup/"make this readable" of findings —
  even if they don't say "HTML." Also use to turn an existing analysis doc or markdown report into a
  friendly visual explainer. Prefer this over a plain markdown summary when the audience is non-expert
  or the user says "pretty," "plain English," "for my boss," "easy to understand," or "report."
author: Claude Code
version: 2.1.0
date: 2026-07-03
---

# show-and-tell — plain-English explainer reports 🎪

Produce a single self-contained HTML page that explains something technical to a smart non-expert —
the kind of report someone forwards to their boss and the boss actually reads. The proven recipe is in
`assets/template.html` (a complete, rendering reference you copy and re-bind). This file is the *why*,
so you don't just fill a template — you make the judgment calls that separate a real explainer from a
prettied-up jargon dump.

## What you're making (and for whom)
A **dual-audience** artifact. The non-expert reads the big text + the metaphor and leaves understanding
the gist and the honest bottom line. The curious/technical reader can drop into the "engineer's note"
asides and the real numbers and find nothing dumbed-down to the point of being *wrong*. The failure mode
on both sides is the same: a report that's either (a) so simplified it's misleading, or (b) so technical
the intended reader bounces. You're threading that needle.

When this fits: the user has just done or received something technical (a debugging session, a research
finding, a measurement, an analysis doc, a migration) and wants it **understandable and shareable**.
When it doesn't: they want the rigorous internal write-up (that's a normal analysis doc), or a live
dashboard (different tool), or slides for a pitch (a deck skill).

## The load-bearing idea: one metaphor, held all the way through
The single biggest quality lever is a **consistent everyday metaphor** that maps *structurally* onto the
real thing, and that you do not abandon halfway. It's the scaffold the non-expert hangs everything on.

- **Pick a metaphor whose parts map to the real parts.** A retrieval system that hides notes and fetches
  the right one on demand → a *filing cabinet + a librarian who hands you the right card*. "Finds it half
  the time / interrupts on everything" → *a librarian who's right half the time but shouts on every
  step*. The mapping has to survive the whole arc, including the bad news — if the metaphor can only
  express the good parts, it's the wrong metaphor.
- **Everyday and concrete beats clever.** Kitchens, librarians, backpacks, mail rooms, traffic, a messy
  desk. Avoid metaphors that themselves need explaining.
- **Name it once, then reuse its vocabulary.** Introduce "the robot librarian" in the hero, then say "the
  librarian" in every later section instead of re-explaining. Consistency is what makes it *click*.
- **One metaphor, not five.** Mixing metaphors is the most common way these reports turn to mush. If you
  need a second image for one section, make it a child of the main one (the librarian's "diary"), not a
  rival.
- It's cheap to try two metaphors in your head and keep the one that carries the *whole* story (good news
  AND limits AND what's next). Do that before you start writing.

## Honesty is the whole point — never trade truth for tidiness
A plain-English report earns trust precisely because it *doesn't* hide the messy parts. This is what
separates it from marketing.

- **Put the real number next to the plain claim.** Don't say "it works pretty well" — say "finds the
  right answer about half the time" *and* show the `~51%` bar. The plain words carry the meaning; the
  number carries the credibility. A claim with no number reads as spin; a number with no plain words
  reads as a spreadsheet. Pair them. (Component: a labelled bar or a stat tile.)
- **Lead with a one-paragraph version** that a reader could stop after and still have the honest gist —
  including the catch, not just the win.
- **Give limits their own box, foregrounded** (not a footnote). "Here's what we're NOT sure of" builds
  more trust than any positive claim. Name the floor-not-ceiling caveats, the small sample, the
  unmeasured bits.
- **If this report corrects an earlier claim (including your own), say so plainly** rather than quietly
  fixing it. "Last time we said X; we tested it and that was wrong" is a trust *builder*, not an
  admission to bury.
- Never invent a number to fill a tile. If you don't have it, the tile says so or it's not there.

## The "engineer's note" — respect the technical reader without taxing the lay one
After a plain-English section, an optional muted aside (`.eng`) gives the precise/technical version: the
real mechanism, the metric name, the exact method. The non-expert's eye skips the muted text; the
engineer drops in. This is how you serve both audiences in one document instead of writing two. Use it
where the plain version genuinely loses something a technical reader would want — not on every section.

## Illustrate the metaphor (optional, high-leverage)
One small picture of the metaphor makes it land faster than any paragraph — a pixel librarian at
her filing cabinet, a pixel kitchen with the oven off. The template ships a `figure.figure`
component (inline SVG + caption) and a worked example. Rules, in priority order:

- **Inline SVG only.** No `<img src>`, no external files, no fonts, no JS — the page must keep
  opening from `file://` offline. (`check_html.py` enforces this.)
- **Every fill/stroke is a `var(--x)`.** A hardcoded hex looks right in arcade and wrong in paper/
  midnight/print. Use the theme tokens (`--neon`, `--coin`, `--violet`, `--ink`, `--panel2`,
  `--track`, `--dim`…) and the art recolours itself when the reader flips the 🎮/📄/🌌 toggle.
- **The picture must carry the bad news too** — same test as the metaphor itself. The template's
  kitchen scene shows the oven *switched off*, not a triumphant chef. If you can't draw the catch
  into it, cut the figure; never let the art oversell what the numbers say.
- **Accessible or invisible:** the `<figure>` gets `role="img"` + an `aria-label` that states what
  the scene shows (the inner `<svg>` is `aria-hidden`); purely decorative flourishes are
  `aria-hidden="true"`.
- **Style: pixel-art fits the arcade theme.** Draw with `<rect>`s on a 7px grid
  (`shape-rendering:crispEdges` is set for you). If the **pixel-art skill**
  (github.com/wan-huiyan/pixel-art) is installed, follow its character/scene conventions — it's the
  same aesthetic; just swap its literal colours for theme vars. A hand-drawn/sketchy look also
  works: 2–3 slightly-jittered overlapping `<path>` strokes, still `var(--x)`-coloured.
- **One hero figure, maybe one spot figure.** This is seasoning, not the meal — text-first, and a
  report with no figure at all is completely fine. Never block a report on art.
- **Fact-check the figure like a claim.** A picture can drift exactly like prose (implying "fixed"
  when the source says "could improve"). The fact-verifier checks captions and aria-labels too —
  feed them in with the report text.

## Structure (the template's spine)
The `assets/template.html` shell, top to bottom — re-bind the content, keep the bones:
1. **Hero** — playful title with the metaphor named; a one-sentence plain framing; a row of "pills" with
   the headline facts (the win AND the catch).
2. **The one-paragraph version** — the honest TL;DR, big text, stoppable.
3. **A reminder of what we were even trying to do** — often a two-card "today (the problem) vs the plan,"
   in metaphor terms, optionally led by the metaphor illustration (`figure.figure`). Skip if the
   audience already knows.
4. **Findings** — one section per real finding. Each pairs a plain claim with its number (bar/tile) and,
   where useful, an engineer's note. Bad news gets a clear callout, not a hedge.
5. **What changed / what we can skip** — concrete outcomes, in plain terms.
6. **Honesty box** — the limits, foregrounded.
7. **What's next** — a short checklist (done vs to-do).
8. **Receipts** — a table of what was produced and where (files, commit), so it's verifiable.
9. **Footer** — date, provenance one-liner.

Not every report needs all nine — drop what doesn't apply (a pure findings recap may skip 3 and 5). Keep
the order; it's the reading rhythm.

## How to build one
1. **Read the source material** (the analysis doc, the transcript, the findings) and extract: the real
   numbers, the bottom line, the limits, and what was produced. Don't proceed on a vague understanding —
   the report is only as honest as your grasp of the facts.
2. **Choose the metaphor** (see above). Sanity-check it carries the bad news too.
3. **Copy `assets/template.html`** to your output path and re-bind each slot. Keep the entire `<style>`
   block + the small theme `<script>` as-is — it's a CSS-variable theme system: arcade (default, dark/
   pixel/fairy-dust) plus **paper** (light, print-friendly) and **midnight**, reader-switchable via the
   top-right 🎮/📄/🌌 toggle. First visit follows the reader's OS light/dark preference (light-mode
   readers get paper); an explicit click is remembered; print forces a clean light theme. Edit
   content, not CSS — and never hardcode
   a colour; every colour is a `--var` so all three themes stay correct.
4. **Write plain.** Short sentences. Second person. Name a thing once in metaphor, then reuse it. If a
   sentence has a piece of jargon the audience won't know, either cut it or move it to an engineer's note.
5. **Pair every claim with its evidence** (number/bar/tile). Add engineer's notes where they earn their
   keep.
6. **Optionally illustrate the metaphor** (see *Illustrate the metaphor*) — one inline-SVG figure,
   theme-var colours, bad news included, or no figure at all.
7. **Fact-check the report against the source** — the honesty gate (see *Fact-check before you ship*).
   A plain-English translation drifts easily; catch it before a stakeholder reads it. Include figure
   captions/aria-labels in what gets checked.
8. **Verify the render** (below) — a broken CSS variable silently turns text invisible.
9. **Open it** for the user: `open <file>.html` (macOS), `xdg-open <file>.html` (Linux), or
   `start <file>.html` (Windows). In a remote/web session where you can't open a browser for them,
   send/attach the file instead — it works the moment they double-click it.

## Fact-check before you ship — the honesty gate
The skill's whole promise is "translate, don't distort." A metaphor or a rounded number drifts from the
source with frightening ease — "could reduce" becomes "will halve," a real figure binds to the wrong
metric, a vivid analogy implies a certainty the findings never had. So before you hand the report over,
**dispatch a separate fact-verifier subagent** (fresh eyes — not the author) given BOTH the original
technical source AND your report. The reusable prompt + the exact checks live in
`references/fact-verifier.md` — it checks number-binding (not just presence), magnitude/causal/metaphor
drift, and material omissions, and it **fails loud** when a claim has no locatable basis (an
"I-couldn't-verify" is a flag, never a silent pass). Fix every DRIFT/FABRICATED/UNVERIFIABLE before
delivering. *Honest limit: an LLM checking an LLM reduces drift, it doesn't eliminate it — for
high-stakes reports a human still skims the source-vs-claim table.*

## Verify the render WITHOUT a screenshot
The page is self-contained (inline CSS, no external fonts, no build, no server — just one tiny inline
script for the theme toggle), so you don't need a browser to catch the likely bugs — and the
Playwright-MCP screenshot subsystem tends to wedge anyway. Run the bundled check — the script lives in
`scripts/` next to this SKILL.md, wherever the skill is installed (`~/.claude/skills/`, a plugin dir,
`~/.cursor/skills/`, …):

```bash
python3 <skill-dir>/scripts/check_html.py <your-report>.html
```

It confirms, in one pass: the HTML parses with balanced tags; every `var(--x)` you reference is
actually defined — the #1 cause of "I opened it and half the text is invisible" is a typo'd or
undefined CSS variable (see `css-var-undefined-silent-declaration-drop`); every theme block
(paper/midnight) overrides the full token set, so switching themes can't leak wrong-contrast colours;
the page stays **self-contained** (no render-time `http(s)` fetches — plain `<a>` links are fine);
figures have text alternatives (`alt`/`aria-label`) and no hardcoded hex colours that would ignore the
theme switcher; and no `__PLACEHOLDER__` slot was left unfilled. For a true visual check, `open`/
`xdg-open`/`start` the file, or serve the directory on a port and use `browser_evaluate` (file:// is
blocked in the MCP browser) — but the static check covers the silent-failure cases.

## Worked example
The skill was extracted from a report that explained a retrieval-system investigation using a "robot
librarian" metaphor — recall shown as "finds it ~51%," precision as "interrupts on ~99.6%," with
engineer's notes, an honesty box, and a correction of an earlier false claim. The template carries a
*different* worked example (a slow nightly job, as a "kitchen") so you can see the recipe generalize.
Read `assets/template.html` top to bottom once before your first build — the inline comments mark each
slot and the intent behind it.

## Keep it honest, keep it kind
The tone is warm and a little playful (the arcade styling is part of that) — but the substance is
straight. You're not spinning; you're translating. The reader should come away understanding *and*
trusting, which only happens if the fun packaging is wrapped around genuinely honest content.
