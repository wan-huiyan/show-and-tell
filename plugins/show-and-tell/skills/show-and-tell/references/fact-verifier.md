# Fact-verifier — does the plain-English report still tell the truth?

This is the honesty gate for a show-and-tell report. A plain-English translation (especially a
metaphor) can quietly *drift* from the technical source — soften a hedge into a promise, bind a
number to the wrong thing, imply cause from correlation, or let the metaphor smuggle a claim the
findings never made. This verifier catches that **before** the report goes to a stakeholder.

Its job is **fidelity to _your_ source** — does the report say what the findings say? — **not**
world-truth. It doesn't check whether the source is *correct*; it checks whether the translation
*drifted*. (That's the distinction from general "fact-check against reality" tools: this one guards
the gap between your findings and your plain-English retelling of them.)

One deliberate exception: a **completion claim** — "done", "merged", "cleared out" — cannot be
settled against a document at all, because a source that describes the work reads as support for
the claim that it finished. Check 9 sends you to the real state instead.

Run it as a SEPARATE subagent (fresh eyes — not the author), given BOTH the original technical
source AND the drafted report. Below is the dispatch prompt; copy it, fill the two inputs, run it,
and fix every DRIFT/FABRICATED/UNVERIFIABLE it returns.

> **Honest limit (carry this):** an LLM checking an LLM *reduces* drift, it does not eliminate it.
> Treat a clean verdict as "no drift I could find," not "provably faithful." For high-stakes
> reports, a human still skims the source-vs-claim table.

---

## Dispatch prompt (fill the two `<<< >>>` inputs)

You are an adversarial fact-checker. Your job is to find every place where a PLAIN-ENGLISH report
has drifted from, overstated, or misrepresented its TECHNICAL SOURCE. You are not here to praise the
writing — you are here to protect the reader from believing something the evidence doesn't support.

**SOURCE (the ground truth — the technical findings/analysis/data):**
<<< paste the complete source here — the analysis doc, the measured numbers, the transcript. >>>

**REPORT (the plain-English explainer to check):**
<<< paste the report's text (or the rendered HTML's visible text) here — INCLUDING any figure
captions and `aria-label` descriptions of illustrations: a picture makes claims too. >>>

### Hard preconditions (FAIL LOUD — do not rubber-stamp)
- If the SOURCE is missing, partial, or you cannot locate it, **STOP and report `CANNOT VERIFY — source not provided/locatable`.** Never pass a report you couldn't check against a source. "I couldn't find the basis" is a FLAG, never a silent pass.
- A claim whose basis you cannot find in the source is **UNVERIFIABLE**, which is a failure to surface — not an OK.

### Check every CLAIM and NUMBER in the report against the source (check 9 against real state), for:
1. **Number fidelity + binding.** Every figure in the report must appear in the source AND be bound to the *same* entity/metric. The classic miss is a real number attached to the wrong thing (e.g. the source's "51% recall / 99.6% fire rate" reported as "51% fire rate") — membership in the source is NOT enough; check what each number is *about*. This includes **sub-group / category binding**: a real number attached to the wrong *subset* — a metric measured on one bucket/segment retold as if it were another (source tested group B; report attributes it to group A). Metaphors that lump distinct groups make this drift especially easy — verify the number lands on the *same* group the source measured.
2. **Magnitude / strength drift** *(the core worry).* The report's confidence must match the source's. Flag softened hedges and inflated certainty: source "could reduce ~30%" → report "will halve"; source "~51%" → report "about two-thirds"; a source *range* collapsed to a single rosy point; "preliminary/estimated" dropped.
3. **Causal / directional drift.** The report must not assert causation where the source shows correlation/association, nor certainty where the source hedges. Check sign/direction too (up vs down, better vs worse, fixed vs mitigated).
4. **Metaphor faithfulness** *(the core worry).* The metaphor must not imply anything the source doesn't support. Test the analogy's implications one by one: if the metaphor says "we just flip the oven on and it's fixed," does the source actually support a clean, low-risk, near-complete fix — or only a partial/uncertain one? A vivid image that overpromises is drift even if no single sentence is false.
5. **Material omission — check BOTH directions** *(the blind spot)*. A material fact the source carried and the report dropped is drift whichever way the drop cuts: the report no longer matches its source.
   - *The omission that flatters.* The source's key caveats/limits/risks must survive into the report's honesty box. Cherry-picking the good news and dropping the "but only on 5 nights / unconfirmed / small sample" is the familiar one.
   - *The omission that alarms.* A **reassuring** fact the source states and the report leaves out is exactly as much drift, and it is the one nobody's instinct catches — a scarier report feels like the safe direction to err in, so nothing gets flagged. (Two real misses on one report, both survived two verifier passes: the source said all 123 cards ended up with a verdict, so no refused save was ever permanent — dropped; the source said the fullest stored card carried 6 items against a cap of 20 — dropped. The report was left more alarming than its own source.)

   Do this as an explicit sweep, not as a feeling: **list every material fact in the source that the report omits, and say for each whether the omission makes the report more alarming or less.** If every entry on that list points the same way, you have only looked one way.
6. **Fabrication.** Any claim or number in the report with NO basis in the source → FABRICATED.
7. **Figure / illustration drift.** An illustration is a claim in pixels. Check each figure's caption
   and aria-label the same way as prose: does the scene imply something the source doesn't support
   (a "fixed!" picture for a "could improve" finding; a triumphant image with the catch missing)?
   The skill's rule is that the picture must carry the bad news too — flag a figure that only shows
   the win, even if every sentence around it is individually accurate.
8. **Invented scope / qualifier.** A figure the source leaves *unscoped* must not gain a scope word in
   the report. A `per-session` / `per-user` / `per-project` / `per-run` qualifier — or an "each" /
   "every" — stapled onto a raw number is drift: the number is right, but its scope is fabricated.
   (Real miss: source "~1.9B tokens re-read" → report "1.9B tokens **per session**".) Watch also for
   the inverse — a source figure that IS scoped ("~248k tokens per session") retold without its scope.
9. **Completion and status claims — check the real state, never the prose.** "Was cleared out", "is fixed", "has been merged", "we deleted them" are claims about the world *now*. A source document that describes the work will read as support for them even while the work is still open, so the source cannot settle these. Go to the state: a pull request's merge status, a file's presence, an issue open or closed, the live deployed revision. If you cannot reach that state from where you are, the claim is **UNVERIFIABLE** — say so rather than accepting the description. (Real miss: a report said 41 stale working copies "were cleared out" while the pull request that clears them was still open. It contradicted its own limits box three paragraphs later and no verifier caught it, because the source *did* describe the clean-up — just not as finished.)

### Output — a per-claim table, an omission list, then a verdict
For EACH checked claim:
| report claim (quote) | source basis (quote or "NONE FOUND") | verdict | severity | suggested fix |
verdict ∈ {FAITHFUL, DRIFT, UNVERIFIABLE, FABRICATED}; severity ∈ {low, med, high}.
List FABRICATED/UNVERIFIABLE/high-severity DRIFT FIRST.

**Then the omission list from check 5, separately** — an omission has no claim to quote, so it falls
straight through a per-claim table and gets skipped. Give it its own rows:
| source fact omitted (quote) | direction (report reads MORE alarming / LESS alarming) | severity | suggested fix |
An omission list that is empty, or that points only one way, is a result to be suspicious of.

Then a one-line **SHIP VERDICT**: `CLEAN` (no drift found) · `FIX-THEN-SHIP` (drift present, fixes listed) · `MAJOR DRIFT` (the report misrepresents the findings — rework). Be concrete in the fixes (the exact wording change), and be honest if the source was too thin to check a given claim.
