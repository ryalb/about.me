---
name: resume-review
description: Review, critique or edit Ryan's bilingual resume in this repo (resume-en_us.json / resume-pt_br.json) and regenerate the md/txt/html/pdf/docx outputs. Use for ATS audits and hiring-manager critiques against a job description, rewriting bullets or summaries, adding certificates/roles/skills, tailoring a version to a role, or any change that must land in both locales and be rebuilt. Triggers on "review my resume", "ATS score", "revisar meu currículo", "tailor to this job", "add this certificate", "rewrite my bullets", "regenerate the resume".
---

# Resume review and editing

Two jobs live here. **Review** (Mode 1) produces critique — no file changes unless asked.
**Edit** (Mode 2) changes resume data and regenerates outputs. A review that ends in
"apply those fixes" becomes Mode 2; run its checklist in full, don't freehand it.

## Orientation (read before touching anything)

- **Source of truth is two files:** `resume-en_us.json` and `resume-pt_br.json`. They are
  parallel documents, not a file plus a translation artifact — the same structure, entry
  counts and dates in both.
- **`latest/en_us/` and `latest/pt_br/` are generated.** Never hand-edit them; they are
  overwritten by `mise run build-all`. `.output/` holds dated build folders.
- **Five formats per locale:** `md`, `txt`, `html`, `pdf`, `docx`. Different code paths own
  them — a fix in one may not appear in another. See `references/pipeline.md`.
- **The JSON is hand-formatted** (keyword arrays inline on one line). Edit with targeted
  string replacement or the Edit tool. Never round-trip the whole file through
  `json.dump` — it reflows everything and buries the real diff.

## Mode 1 — Review

Adopt the stance of a senior hiring manager at a top-tier company **and** a strict ATS
specialist. Be blunt. Sugarcoating wastes the user's time; a resume that passes a friendly
review and fails a real screen is the bad outcome.

**Before scoring, you need a target.** If no job description or target role was given, ask
for it — an ATS score without a JD is invented precision. If the user wants a general
review instead, say that's what you're doing and score against role-typical expectations
rather than claiming a JD match.

### Phase 1 — Brutal audit and ATS match

- Compatibility score out of 100 against the JD. Break the number into components so it's
  arguable, not oracular (see `references/review-rubric.md`).
- The top 5 missing keywords or hard skills. Distinguish **absent from the resume** (a
  writing gap — fixable now) from **absent from the user's experience** (a candidacy gap —
  do not paper over it).
- 3 major red flags, weak points or clichés that would sink this in a 10-second scan.
  Quote the offending text with its `file:line`. "Be specific" applies to your critique too.

### Phase 2 — Bullet transformation

Rewrite bullets as **Action verb + task + measurable result**, or Google XYZ:
"Accomplished [X], measured by [Y], by doing [Z]".

**When a metric is missing, ask — never invent one.** Ask targeted questions **one at a
time**, and prefer questions the user can actually answer from memory ("roughly how many
requests/day did that service handle?" beats "what was the ROI?"). Deliver the rewritten
bullets that don't need metrics immediately; don't block the whole phase on one unknown.

Every rewrite must stay traceable to something already in the JSON. If a claim isn't
supported by an existing `highlights` entry, it is either a question for the user or it
doesn't ship.

### Phase 3 — Tone and final polish

- Summary and skills language against top-company norms; strip generic phrasing.
- Tense consistency (present for the current role, past for prior roles) and passive →
  active voice.
- **Then check the ATS-hostile formatting** specific to this repo's outputs — multi-column
  layout, icon glyphs, the right artifact to actually submit. Details in
  `references/review-rubric.md`. A perfect bullet inside an unparseable PDF still fails.

Report per-locale when the two files diverge. They drift; assume nothing is symmetric until
you check (see the parity command in `references/pipeline.md`).

## Mode 2 — Edit

1. **Read the target entries in both files first.** Confirm the field exists and how
   sibling entries are phrased; match the surrounding voice (`summary` fields are noun
   phrases; en_US `highlights` open with a past-tense verb, pt_BR `highlights` are written
   in first person).
2. **Check the renderers support the field** before designing data around it. Adding a key
   nothing reads is invisible work — e.g. `certificates` renders only
   `name`/`date`/`issuer`/`url`, so anything else (hours, module list) has to fold into
   `name` or be dropped deliberately.
3. **Apply to both locales.** An en_US-only edit is an unfinished edit. Keep tool, product
   and standard names untranslated (`Certified ScrumMaster`, `Kubernetes`, `JSON:API`);
   translate prose.
4. **Rebuild:** `mise run build-all`.
5. **Verify in the format that matters** — not just the one that's easy to grep. HTML
   passing tells you nothing about the PDF; they use different layout engines.
6. **Check page counts** with `pdfinfo`. pt_BR prose runs ~20–25% longer than en_US, so
   Portuguese edits push page boundaries first. If a change adds a page, tighten the text
   and rebuild before reporting.
7. **`mise run check` must pass first time.** `build-all` runs it once, and the generator
   emits text that already satisfies the whitespace/EOF hooks. A failure is a real failure —
   fix it, don't re-run. Don't report a passing gate you haven't actually seen pass.
8. **Report honestly:** what changed, which assumptions you made, what you deliberately
   left out and why. Flag data problems you noticed but didn't fix rather than silently
   fixing or silently ignoring them.

## Hard rules

- **Never fabricate a credential, metric, date, employer or technology.** This is a
  document a real person submits under their own name. Everything traces to the JSON or to
  something the user told you in this conversation. Uncertain → ask.
- **Never hand-edit `latest/`.** Change the JSON (or the theme/renderer) and rebuild.
- **Both locales, every time.**
- **Don't weaken a factual claim to make a sentence prettier**, and don't strengthen one
  to make it punchier. "Contributed to CMM Level 2 certification" is not "achieved CMM
  Level 2".
- **Age-bias hygiene:** birthdate is intentionally absent (`meta.notes`). Don't add it, and
  don't add anything that functions as a proxy for it.
- **Verify claims that decay.** Year counts ("26 years"), "top 2026 contributor" and
  "present" roles go stale. Recompute from the earliest `startDate` rather than trusting
  the existing prose.

## Before claiming done

- [ ] Change present in **both** JSON files
- [ ] `mise run build-all` succeeded (5/5 files per locale)
- [ ] Verified in every format the change can reach — including PDF
- [ ] Page counts checked; no unintended new page
- [ ] `mise run check` green on the first run
- [ ] Report states what you assumed and what you left undone
