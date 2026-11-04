---
name: show-and-tell
description: >
  Turn dense technical findings, an analysis, a code/research session outcome, or a jargon-heavy
  document into a genuinely PLAIN-ENGLISH self-contained HTML explainer a non-technical or busy
  stakeholder can actually understand AND trust — built on a single everyday metaphor carried through
  the whole piece (the bad news included), picture-first with a hard word budget (every finding drawn
  however shows it best — scenes, cartoons, diagrams — animated only when the point is a change), with the REAL numbers shown honestly
  beside each plain claim, an "engineer's note" layer so technical readers aren't shortchanged, a foregrounded
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
version: 2.5.0
date: 2026-11-04
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

**If the report ends in a decision the reader must make, it gets `promptback` widgets — standing
preference, see the section below.** When this fits: the user has just done or received something technical (a debugging session, a research
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
- **On number-dense findings, keep the metaphor light — it is itself a drift surface.** A metaphor that
  lumps distinct sub-groups is a common source of *binding drift* (a stat lands on the wrong group), and
  vivid prose invites invented scope words ("per session", "every run") the source never stated. Let the
  engineer's-notes and the honesty box carry the precise sub-group boundaries and scopes. This is an
  observed failure mode — your own careful draft can drift a number even when a plain summary wouldn't;
  that is exactly why the fact-verifier (checks #1 and #8) is not optional.

## Honesty is the whole point — never trade truth for tidiness
A plain-English report earns trust precisely because it *doesn't* hide the messy parts. This is what
separates it from marketing.

- **Put the real number next to the plain claim.** Don't say "it works pretty well" — say "finds the
  right answer about half the time" *and* show the `~51%` bar. The plain words carry the meaning; the
  number carries the credibility. A claim with no number reads as spin; a number with no plain words
  reads as a spreadsheet. Pair them. (Component: a labelled bar or a stat tile.)
- **Lead with a short version** (≤40 words) that a reader could stop after and still have the honest
  gist — including the catch, not just the win.
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

## Pictures first, few words — the eli5 rule
The reader looks before they read, and most stop reading early. Borrowed from the `eli5` skill's brief
— *big pictures, few words*. Like eli5, **the drawing method is yours to choose.** Draw whatever makes
this finding land: a scene with characters, a cartoon, a cutaway, a map, a comic strip, a machine
with its parts labelled, a before/after pair, a crowd of little people, emoji arranged into a picture,
CSS art, a chart if a chart is truly clearest. Pictures are big — give a strong one
the full width. Don't default to a bar chart or a row of boxes because they are easy; that is the
spreadsheet coming back in through the side door.

Only these rules are fixed, because each one protects the reader:

- **The picture shows the finding, not just the setting.** A chef standing in a kitchen is scenery; the
  same chef wearily re-chopping a pile of onions stamped "yesterday's", while the shiny oven behind
  them sits unplugged, is the finding. Write the finding as one sentence first, then draw that
  sentence.
- **Cover test.** Hide the caption. Can someone say the finding from the picture alone? If not, redraw
  — don't add words. Labels inside the picture are fine; keep them short.
- **The picture carries the bad news too.** If the catch isn't drawn, it sits right under the picture.
  An estimate looks like one (dashed, faded, "est."), never as solid as a measurement. If you can't
  draw the catch in, the picture is overselling — change it.
- **Numbers drawn are numbers claimed.** If the picture shows a quantity (7 of 10 trays, a bar's
  length), it must match the source, and the caption states the real figure.
- **The `aria-label` is the one-sentence finding**, so a screen reader — and the fact-verifier — get the
  claim, not a description of a scene.
- **Self-contained, and complete without JS.** The page must open from `file://` with no network:
  inline SVG, CSS, emoji, or `data:` images are all fine; nothing fetched at render time. Avoid
  `<canvas>` — it is blank without JS and the fact-verifier can't read it.
- **Readable in every theme.** Use the theme `var(--x)` colours and the drawing follows the 🎮/📄/🌌
  toggle by itself. If the picture needs its own palette (skin tones, a sunset, a gradient), give the
  figure `data-palette="own"` and draw it on its own background inside the figure so its contrast never
  depends on the theme — `check_html.py` then allows hardcoded colours inside that figure only.
- **Fact-check the picture like a claim.** A drawing drifts exactly like prose. Feed captions and
  aria-labels to the fact-verifier with the report text.

### The word budget
`check_html.py` fails the page when it goes over:

- **≤60 visible words** in the hero and in each section; **≤350** on the whole page.
- The short version is **≤40 words** and still includes the catch.
- Engineer's notes go in a collapsed `<details class="eng">` (opened automatically for printing) and
  don't count. Nor do tables, SVG text, or the footer.
- **The honesty box counts and is never collapsed.** Meet the budget by drawing, never by hiding the
  catch where nobody will open it.
- If a report can't fit, it's two reports.

### Animate only when the point is a change
Follow the `animate` skill's rules. In a report its gate comes out as: purpose = *explanation*, seen
once → motion is allowed, but **only when the finding is itself a change or a sequence** — a bar growing
past a deadline, items piling up, a cause reaching its effect. A share or a count gets a static picture,
or at most a quick build-in.

- **Use the template's machinery, don't write new.** Put `class="figure animated"` on the figure and
  `class="anim pop|stamp|run"` on the SVG elements that move; stagger with inline `animation-delay`
  steps of 30–80ms. Each figure plays once, when it scrolls into view. No loops beside text.
- **The base style is the final frame.** The keyframes only define where motion starts. With no JS,
  under reduced motion, and in print the figure never arms, so the reader sees the final frame — which
  therefore has to carry the point *and* the catch on its own.
- `transform` and `opacity` only; easing from the `--ease-out` token (taken from the `animate` skill's
  table), never a hand-made curve.
- **Motion makes claims too.** A bar animating from 4h down to 2h says "will halve." If the source says
  "could," the end state says "est." — and the fact-verifier checks the end state.

## Structure (the template's spine)
The `assets/template.html` shell, top to bottom — re-bind the content, keep the bones:
1. **Hero** — playful title with the metaphor named; a one-sentence plain framing; a row of "pills" with
   the headline facts (the win AND the catch).
2. **The short version** — the honest TL;DR in ≤40 words, stoppable, catch included.
3. **A reminder of what we were even trying to do** — often a two-card "today (the problem) vs the plan,"
   in metaphor terms. Skip if the audience already knows.
4. **Findings** — one section per real finding, led by its picture (`figure.figure`) with the number in
   the caption, then at most a line or a callout, then a collapsed engineer's note. Bad news gets a
   clear callout, not a hedge.
5. **What changed / what we can skip** — concrete outcomes, in plain terms.
6. **Honesty box** — the limits, foregrounded.
7. **What's next** — a short checklist (done vs to-do).
8. **Receipts** — a table of what was produced and where (files, commit), so it's verifiable.
9. **Footer** — date, provenance one-liner.

Not every report needs all nine — drop what doesn't apply (a pure findings recap may skip 3 and 5). Keep
the order; it's the reading rhythm.

## If the report ASKS the reader anything, make it tickable — use `promptback` (standing preference)

**Owner's standing preference, set 2026-08-06: any show-and-tell that ends in a decision the reader has
to make gets `promptback` widgets. Do not ship a decisions section the reader has to retype answers to.**

The trigger is narrow and mechanical: **does the page contain a question only the reader can answer?**
A findings recap with no ask stays a flat page — adding widgets to it is noise. But the moment there is
a "should we…", an options list, or a "waiting on you", the reader is being asked to produce structured
output from unstructured reading, and a flat page makes them do that from memory in a chat box.

Load `promptback` and follow it; the pieces that matter here:

- **One widget per question**, immediately under that question's own context — not collected into a form
  at the end. The reader decides while the argument is still in front of them.
- **Question-specific chips**, never generic approve/revise. The copied prompt should read
  `[MUZZLE-AND-TAIL]`, not `[APPROVE]`.
- **The token in the chip must be decoded, verbatim, in the widget's own meaning line AND in the copied
  prompt's "Meaning of ticks" section.** On a recommendation-shaped question a bare `[YES]` is ambiguous
  to the receiving session — yes to the change, or yes to the status quo the report defended? A page
  shipped 2026-08-06 had a chip whose value was `both` against a legend that only said "Muzzle + tail";
  the token and its key never met, and only a test caught it.
- **Keep the narrative order.** `promptback` says put decision items first, and that is right for a pure
  triage page. It is wrong here: an explainer earns its decisions by explaining first. Reconcile the two
  with the fixed dock — it is visible from the top of the page and carries the answered count, so the
  reader always knows there is something to do without the page being reordered around it.

**And the honesty rule still outranks the widget.** If a question is no longer the reader's to answer —
someone else picked it up, or it got settled while you were writing — delete the widget and say so in
plain text. A tickable question that is already being worked on wastes the one thing the page is
spending: their attention.

## How to build one
1. **Run an eli5 pass first, and keep what it finds.** Before touching the source, explain each
   finding to yourself in the style of the `eli5` skill (github.com/anthropics/claude-plugins-community —
   installed as `eli5@claude-community`): someone who knows nothing, one sentence, picture-first, no
   jargon. Borrow its brief rather than invoking `/eli5`, which publishes its own separate page; this
   report has to stay one self-contained file. Keep the output — it is the plan for the report: the
   metaphor, the one sentence per finding, and the picture that shows each sentence (a count, a
   comparison, or a cause). If a finding has no clean picture, it is probably two findings.
2. **Read the source material** (the analysis doc, the transcript, the findings) and extract: the real
   numbers, the bottom line, the limits, and what was produced. Don't proceed on a vague understanding —
   the report is only as honest as your grasp of the facts.
3. **Choose the metaphor** (see above), starting from what the framing pass in step 1 surfaced — keep it
   if it survives contact with the real numbers and the bad news, swap it if it doesn't. Sanity-check it
   carries the bad news too.
4. **Copy `assets/template.html`** to your output path and re-bind each slot. Keep the entire `<style>`
   block + the small theme `<script>` as-is — it's a CSS-variable theme system: arcade (default, dark/
   pixel/fairy-dust) plus **paper** (light, print-friendly) and **midnight**, reader-switchable via the
   top-right 🎮/📄/🌌 toggle. First visit follows the reader's OS light/dark preference (light-mode
   readers get paper); an explicit click is remembered; print forces a clean light theme. Edit
   content, not CSS — and never hardcode
   a colour; every colour is a `--var` so all three themes stay correct.
5. **Write plain, and little.** Short sentences. Second person. Name a thing once in metaphor, then
   reuse it. Stay inside the word budget; jargon and method go in a collapsed engineer's note.
6. **Pair every claim with its evidence** (number/bar/tile). Add engineer's notes where they earn their
   keep.
7. **Draw each finding** (see *Pictures first*) — any method that lands; the cover test passes and
   the catch is drawn. Animate it only if the finding is a change.
8. **Fact-check the report against the source** — the honesty gate (see *Fact-check before you ship*).
   A plain-English translation drifts easily; catch it before a stakeholder reads it. Include figure
   captions/aria-labels in what gets checked.
9. **Verify the render** (below) — a broken CSS variable silently turns text invisible. **Look at every
   figure** at desktop and 390px width (labels collide in monospace before they do anywhere else), and
   if anything animates, also with reduced motion on and in print: both must show the final frame. **If you added
   promptback widgets, verify them by DRIVING them, not by reading the HTML** — the copied text is
   assembled at runtime from hand-written `data-` attributes, and a chip that fails to persist or a key
   with a hole in it looks perfect on screen. Chrome is not always reachable (the extension was down the
   day this was written), so prefer a headless harness that loads the page's own script into a fake DOM
   over a browser check that may not be runnable. The harness needs to do three things: run the page's
   own `<script>` against a minimal DOM, drive a chip and a note, and assert the copied text contains
   the token AND its decoding. Wire it into your repo's test suite so it keeps running.
10. **Open it** for the user: `open <file>.html` (macOS), `xdg-open <file>.html` (Linux), or
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
delivering.

Two of its checks exist because the verifier itself missed them on real work, and they are the two
easiest to skim past:

- **Omissions count in BOTH directions** (check 5). Dropping a caveat is the one everyone looks for.
  Dropping a *reassuring* fact the source stated leaves the report more alarming than its own
  source, and nobody's instinct flags it — a scarier report feels like the safe way to be wrong.
  The verifier now lists omissions separately from the per-claim table, because an omission has no
  claim to quote and falls straight through a table of quotes.
- **"Done" is checked against real state, not against prose** (check 9). A source that describes the
  clean-up reads as support for "was cleared out" while the pull request doing it is still open.

*Honest limit: an LLM checking an LLM reduces drift, it doesn't eliminate it — for
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

**Read a pass as exactly what it is.** `check_html.py` validates the page's *structure*. It does
**not** parse attribute values, it does **not** execute the page, and it does **not** lay the page
out — so a page can pass it with its interactive half dead or its content running off the side of a
phone. Two measured examples:

- On a page this checker otherwise passes, one widget whose options sat in a single-quoted
  attribute containing an unescaped apostrophe rendered with **no working widget at all**, and
  `check_html.py` returned **exit 0, CLEAN** — the same verdict, word for word, as on the working
  page. (Its two reports differ only in the filename it echoes back on line 1.)
- A long file path in a receipts cell has nowhere to break, so it pushes the whole page sideways.
  Two real reports measured **527px and 691px wide inside a 390px viewport**. Fixed in the template
  as of v2.3.0, but the general point stands: **load the page and read `document.documentElement
  .scrollWidth` against `clientWidth` at 390px** before you hand it over. A screenshot will not tell
  you — headless Chrome has a ~500px floor, so a "390px" picture is a crop of a 500px layout.

## Worked example
The skill was extracted from a report that explained a retrieval-system investigation using a "robot
librarian" metaphor — recall shown as "finds it ~51%," precision as "interrupts on ~99.6%," with
engineer's notes, an honesty box, and a correction of an earlier false claim. The template carries a
*different* worked example (a slow nightly job, as a "kitchen") so you can see the recipe generalize:
two pictures, both animated, both readable as a still: a scene (a tired chef re-chopping seven of
yesterday's onions while the oven sits unplugged) and, because there a chart really is clearest,
tonight's run vs the estimate against the 6am bell. Draw yours however the finding lands best.
Read `assets/template.html` top to bottom once before your first build — the inline comments mark each
slot and the intent behind it.

## Keep it honest, keep it kind
The tone is warm and a little playful (the arcade styling is part of that) — but the substance is
straight. You're not spinning; you're translating. The reader should come away understanding *and*
trusting, which only happens if the fun packaging is wrapped around genuinely honest content.
