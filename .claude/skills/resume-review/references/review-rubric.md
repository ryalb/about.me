# Review rubric

Expansion of Phases 1–3 in `SKILL.md`. The point of a rubric is that the user can argue
with a number instead of being handed one.

## Scoring (out of 100)

Score components, show the arithmetic, then the total. Suggested weights — adjust to the JD
and say so when you do:

| Component | Weight | What it measures |
| --- | --- | --- |
| Hard-skill / keyword coverage | 30 | JD must-haves present *in the resume text*, not just in the person |
| Evidence of impact | 25 | Bullets with a measurable result vs. bullets that only describe activity |
| Seniority and scope fit | 20 | Does the scope of work match the level advertised |
| Domain / industry fit | 15 | Same problem space, or a credible adjacency |
| Screen readability | 10 | Does the top third earn a 10-second scan; ATS parseability |

Rules that keep the number honest:

- **No JD, no match score.** Score against role-typical expectations and label it as such.
- Cite evidence for each component — `resume-en_us.json` line or the JD phrase. An
  uncited score is a guess with decoration.
- Separate **resume gap** (present in the person's history, missing from the document) from
  **candidacy gap** (genuinely absent experience). The first is worth fixing in the next
  hour; conflating them is how a candidate gets talked out of applying.
- Score the locale being submitted. en_US and pt_BR are not interchangeable.

## Keyword extraction from the JD

1. Pull explicit hard requirements (languages, frameworks, platforms, certifications,
   years).
2. Pull implicit ones (a "Kubernetes-native platform" role implies Helm, container
   registries, CI/CD).
3. For each, grep both JSON files — the term may exist in `skills.keywords` or a `work`
   entry's `keywords` but never appear in readable prose. **ATS parsers read the document
   text, not your tagging scheme**, so a keyword that only lives in `keywords` and never
   surfaces in a `summary` or `highlights` bullet is effectively missing. Say so.
4. Rank the 5 that would most change the screening outcome. Not the 5 easiest to add.

## Red-flag catalogue

Look for these before inventing new criticisms:

- **Clichés and unfalsifiable traits** — "team player", "hardworking", "passionate",
  "detail-oriented", "results-driven", "ninja/rockstar/guru".
- **Activity described as achievement** — "responsible for", "worked on", "helped with",
  "involved in", "assisted". No outcome, no number, no consequence.
- **Unquantified superlatives** — "significantly improved", "greatly reduced",
  "dramatically increased" with no figure attached.
- **Buried lede** — the strongest, most recent, most relevant work sitting below three
  paragraphs of history.
- **Wall of text** — a summary long enough that a recruiter skips it entirely.
- **Tech-list-as-bullet** — a bullet that is just a comma-separated stack with no verb.
- **Stale framing** — year counts, "currently", "present" and year-stamped claims that no
  longer hold.
- **Unexplained gaps or same-employer sprawl** that reads as stagnation when it was
  actually role progression. (This resume is a long single-employer history across many
  distinct roles — make sure the *progression* is legible, since that's the real story.)
- **A role summary that contradicts its own bullets** — check every `work` entry's `summary`
  and `position` against its `highlights`, not just the prose in isolation. Look for counts
  that no longer add up ("four internal platforms" over five bullets), a summary or position
  qualifier naming a stack the bullets no longer use, and bullets the summary never accounts
  for. This is the most common form of drift in this file, because edits land on bullets and
  the summary is a level of zoom nobody re-reads.
- **Seniority mismatch in voice** — a principal-level history written in junior-level
  language, or the reverse.

For each flag: quote it, name why a recruiter rejects on it, then give the concrete
replacement. Criticism without a rewrite is just noise.

## Bullet rewriting

Formula: **Action verb + task + measurable result**, or XYZ: "Accomplished [X], measured by
[Y], by doing [Z]".

- Lead with the outcome when the outcome is the impressive part; lead with the action when
  the *how* is the differentiator.
- One idea per bullet. Two achievements in one bullet means neither gets read.
- Keep the verb tense consistent with the role's status (current role → present tense).
- Preserve any hedge that exists in the source data. "Contributed to CMM Level 2
  certification" and "raised scores by approximately 20%" keep their qualifiers.
- Prefer numbers the user can defend in an interview over numbers that merely sound big.

### Asking for missing metrics

One question at a time. Make each answerable from memory:

> That onboarding platform replaced a manual nine-step process — roughly how long did the
> manual version take per new hire, and how long does it take now?

Good targets: volume (requests, records, repos, users), time (before → after), team size,
frequency, cost, error/defect rate, adoption. Deliver every rewrite that doesn't depend on
an unknown while you wait for the answer.

## ATS-parseability of this repo's outputs

This matters as much as the wording, and it's specific to how these files are built:

- **`txt` and `docx` are the ATS-safe artifacts.** Single-column, plain text, no icon
  glyphs. When someone asks "which file do I upload to the portal", these are the answer
  unless the posting demands PDF.
- **The `pdf`/`html` skills section is a two-column card grid.** Human-readable and
  attractive; some ATS parsers linearize multi-column layouts badly, interleaving the two
  columns. Flag this when the target is a portal known to be strict, and point at the
  `txt`/`docx` alternative rather than redesigning the theme.
- **Contact line uses inline MDI icon SVGs.** Fine for humans and for the text renderers
  (which emit plain text), but PDF text extraction can drop or mangle glyphs — check with
  `pdftotext` before asserting the phone/email parse cleanly.
- **There is an `ats` summary variant** in `meta.summaries` — keyword-dense, plainly
  worded. `--summary ats` is the right build for portal submissions. Check it's still in
  step with `basics.summary` before recommending it.
- **Dates are `YYYY-MM` in md/txt/docx and formatted (`Jan 2026`) in html/pdf.** Both parse;
  don't "fix" one to match the other without a reason.

## Output shape

Lead with the score and the three red flags — that's what the user needs first. Then
keywords, then rewrites. Keep Phase 2 rewrites in a copy-pasteable form (the exact JSON
string, when the next step is an edit). Close with what you'd need from the user to go
further, phrased as one question, not a survey.
