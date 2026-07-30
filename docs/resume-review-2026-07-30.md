# Resume review — open items

**Date:** 2026-07-30 (pending only; completed work removed — see git history for the diff)
**Files:** `resume-en_us.json`, `resume-pt_br.json` + generated artifacts in `latest/`
**Target:** no job description. Anything scored here is against **role-typical expectations
for a Senior/Staff backend engineer in 2026**, not a JD match.
**Portuguese:** [`resume-review-2026-07-30.pt_br.md`](resume-review-2026-07-30.pt_br.md)

Tracks A, B and C are **done**: summaries trimmed (en 172→96 words, pt 217→113), decaying
claims and editorialising removed, locale parity restored, the LinkedIn URL made extractable
in all five formats, pt_BR section headers localised, `--cut-date` stopped deleting degrees,
and `mise run short` added (3 pages vs the 6-page master).

**One finding from the original review was withdrawn as wrong:** `meta.summaries.platform`'s
"25 years" does not contradict `basics.summary`'s "26 years" — they measure build/release/CM
ownership (from `2001-10`, 24.8 yrs) and career length (from `2000-06`, 26.2 yrs). Both correct.

---

## Where the score actually stands

**Evidence of impact is still 9/25, unchanged.** Nothing in tracks A–C moved it, by design —
those fixed wording, contradictions and tooling. Impact measures quantified outcomes, and the
document still contains exactly one, from a role that ended in **2005**
(`resume-en_us.json:115`, "…by approximately 20%").

Everything recent still counts *artifacts built* — nine dashboards, five repositories, four
apps, six tools — rather than outcomes. **Only P1–P4 change that number.** Everything else
below is secondary.

---

## Blocking — needs your answer

### Metrics (highest leverage, in order)

| # | Question | Where it lands |
|---|---|---|
| **P1** | The onboarding platform replaced a manual nine-step process — roughly how long did onboarding one new hire take **before**, and how long **now**? | `:32` both locales. Turns your flagship recent solo build into the only quantified recent outcome. Answer this one first. |
| **P2** | Across those nine years of Scrum technical direction: how many engineers, over how many teams? | `:68` both locales. Currently the weakest bullet in the document — nine years of leadership stated as a list of ceremonies. |
| **P3** | The "nationwide" production platform: traffic, users or request volume? | `:85` both locales. "Nationwide" is the largest scale word in the resume and carries no number. |
| **P4** | Test coverage **before → after** across the five repositories? | `:37` both locales. Would replace "thousands of tests", which reads as volume rather than result. |

### Facts I can't infer

| # | Question | Why it matters |
|---|---|---|
| **P5** | Have you used **Terraform**, or another IaC tool, in production? | Ansible, Helm and Kustomize are present; Terraform appears nowhere. This is either a resume gap (fixable now) or a candidacy gap (not to be papered over) and I can't tell which. |
| **P6** | Did you personally own **observability** work — OpenTelemetry, Sentry? | They sit in `skills.keywords` only (en `:260`, pt `:250`) and never appear in a highlight. ATS parsers read document prose, not your tagging scheme, so as written they are effectively absent. If you owned it, it needs a bullet; if it was ambient, it should probably leave the keywords. |
| **P7** | Who have you **mentored** since 2009, and roughly how many? | `Mentoring` / `Mentoria` is a keyword (en `:270`, pt `:260`) but the last leadership bullet in the document is from the 2005–2009 role. |

### Decisions

| # | Decision | Notes |
|---|---|---|
| **P8** | Adjacent duplicate job titles: **merge** each pair into one entry, or **differentiate** the titles by scope? | Three of four adjacent pairs share an identical `position` — entries 1&2 "Senior Backend Software Engineer", 3&4 "Senior Full-Stack Software Engineer", 7&8 "Junior Software Engineer". A scanner reading the same title twice in a row reads *padding*, when the real story is 26 years of progression. Differentiating needs facts I don't have. **This is the real page-count lever.** |
| **P9** | Current-role tense: keep the house past-tense convention, or use present tense for the ongoing role? | `work[0]` correctly has no `endDate`, but its en_US highlights read "Built solo", "Shipped", "Delivered". `SKILL.md` documents past tense as the convention; a hiring manager reads present tense as still-doing-this. A genuine trade-off, not a bug. |
| **P10** | `https://shorturl.at/p0ZhO` in the education summary (`:157` both locales): canonical dissertation URL, drop the parenthetical, or leave it? | Shorteners read as link-rot risk and some parsers strip them. I can resolve the redirect if you'd rather I find the real URL. |
| **P11** | `awards[0].links` — **see the warning below.** Teach the renderers, fold into `summary`, or drop? | Live parity break plus dead data. |
| **P12** | Skills two-column grid: accept it and submit `txt`/`docx` to strict portals, or make the print layout single-column? | Under plain `pdftotext` (how most ATS parsers read a PDF) the columns interleave, the "Expert"/"Advanced" levels detach from their categories and invert, and `Multi-arch builds` splits into `Multi-` / `arch builds`. **Recommend accept + document** — the rubric advises against redesigning the theme, and `txt`/`docx` are already single-column and ATS-safe. |
| **P13** | `basics.label` is "Senior Software Engineer" (`:5` both locales) — retitle? | The scope described is Staff+: a 10-engineer team, company-wide standards, a CMMI L3 appraisal as a trained SCAMPI evaluator, four platforms built solo. You under-claim. Your call; I won't invent a title you don't hold. |
| **P14** | Three of four publications still have **no verifiable URL**. Do you have PDFs, or a personal/institutional page you control? | KSACI is now linked to its Springer chapter. The other three are 2001–2008 papers from small venues (a Brazilian SBC workshop, an AAMAS side workshop, a BCS special-interest group) that appear never to have been assigned a DOI. KEOPS is findable only as a citation inside other people's bibliographies; the WJOGOS and BCS-CMSG papers return zero results on every reachable index. A page you own is a more durable link than a publisher record that does not exist. |
| **P15** | KSACI `releaseDate` is `2001`, but Springer publishes the volume as **2002** (ATAL was August 2001; *Intelligent Agents VIII* was published 21 June 2002). Keep the conference year or switch to the publication year? | Both are defensible citation conventions. Left at `2001`; say the word and I will change it. |
| **P16** | Springer lists the third author as **"Gustavo E. de Paula"**; your data had "G. Eliano de Paula". | Only matters if you want co-author names back in the summaries (they were removed — see the note under §7). Flagging so the record is not lost. |

---

## ⚠ New problem introduced since the review

**`awards[0].links` is dead data and breaks locale parity.**

Two link objects were added to `resume-en_us.json` (Sea Hunter gameplay video, JAR download).
Verified: the field renders in **zero of five formats**.

```
$ grep -ciE 'youtube|phoneky|gameplay' resume.md resume.txt resume.html   → 0 0 0
$ pdftotext resume.pdf - | grep -ciE 'youtube|phoneky|gameplay'           → 0
$ unzip -p resume.docx word/document.xml | grep -ciE 'youtube|phoneky'    → 0
```

Every renderer reads only `title` / `date` / `awarder` / `summary` / `url` from an award, and
unknown fields are silently ignored. Two further issues:

- **pt_BR does not have it** — an en_US-only edit is an unfinished edit.
- **Schema validation may reject it** once network validation actually runs (it was skipped
  offline during my builds), depending on whether the JSON Resume schema permits extra
  properties on an award.

Three ways out (**P11**): teach the renderers to emit `links` — touches all four Python
renderers plus the theme, the same five-path job as the LinkedIn fix; fold the two URLs into
the award's `summary`, where they will actually render; or drop the field. Note
`awards[0].url` already points at the Optus press release and does render.

---

## Known, unfixed, not blocking

| Item | State |
|---|---|
| **Master is still 6 pages**, both locales | Trimming the summary freed ~⅓ page; the bullet split and the longer, better `work[2]` bullet consumed it again. Addressed for submissions by `mise run short` (**3 pages**, degrees preserved). Shrinking the *master* depends on **P8**. |
| **Skills render on page 4 of 6** in the master PDF | Follows from the page count. The short variant puts them on page 1. |
| **Section order differs between formats** | `md`/`txt`: Work → Education → Skills → Awards → Certifications → Publications → Languages. `pdf`/`html`: Experience → Skills → Education → Publications → Awards → Languages → Certificates. Neither is wrong, but "what a recruiter sees first" has to be tuned twice. Small change to unify if you want it. |

---

## Recommended order

1. **P1** — one answer, the biggest single movement in the score.
2. **P2–P4** — the rest of the metrics. Together these are the only thing that lifts impact
   above 9/25.
3. **P11** — small, and it's a live parity break plus a possible validation failure.
4. **P5–P7** — resolve whether each is a resume gap or a candidacy gap.
5. **P8** — structural; measure page counts once, after it lands.
6. **P9, P10, P12, P13** — polish and judgement calls.
