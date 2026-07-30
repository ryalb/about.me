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

**Score: 65 → 72/100.** Two components moved, both from answers you supplied:

| Component | Weight | Was | Now | Why |
|---|---|---|---|---|
| Hard-skill / keyword coverage | 30 | 25 | 25 | unchanged |
| Evidence of impact | 25 | 9 | **13** | P4 gave the first quantified *recent* outcome — coverage 0% → ~80% on one repository and ~50% → ~80% on four more. Before this, the document's only number was from a role that ended in 2005. |
| Seniority & scope fit | 20 | 15 | **16** | P2 put team size on the page (6–15 engineers across four projects), so the leadership claim now has scope. |
| Domain / industry fit | 15 | 13 | 13 | unchanged |
| Screen readability | 10 | 3 | **5** | The 172-word opener is gone and pt_BR headings are localised; still 6 pages with skills on page 4. |

**All four metric questions are now closed, and 13/25 is the ceiling for the moment.** The
coverage bullet is the only recent quantified outcome; everywhere else the recent work still
counts artifacts — nine dashboards, four apps, six tools. Both remaining routes are blocked on
reality rather than on writing: P3's traffic data does not exist, and the onboarding platform
has not been measured in production yet (see below). Revisit when it has.

---

## Blocking — needs your answer

### Facts I can't infer

| # | Question | Why it matters |
|---|---|---|
| **P6** | Did you personally own **observability** work — OpenTelemetry, Sentry? | They sit in `skills.keywords` only (en `:260`, pt `:250`) and never appear in a highlight. ATS parsers read document prose, not your tagging scheme, so as written they are effectively absent. If you owned it, it needs a bullet; if it was ambient, it should probably leave the keywords. |

### Decisions

| # | Decision | Notes |
|---|---|---|

---

## Resolved: `awards[].links` is intentional reference data

**Decision: keep it, unrendered.** The two Sea Hunter links (gameplay video, JAR download)
stay in the source as reference material for future use. They render in **zero of five
formats** — which is now the intended behaviour, not a defect. Every renderer reads only
`title` / `date` / `awarder` / `summary` / `url` from an award and ignores unknown fields.

Two things were fixed to make that safe:

- **Mirrored to pt_BR**, with translated labels. The rule is both locales every time, even for
  data nothing renders — otherwise the files drift and the next parity check flags it.
- **Documented in `meta.notes`** in both files, so this is not re-flagged as dead data by a
  future review. The note records that the field is deliberate, non-rendering, and legal.

**Schema risk: cleared.** I could not reach the schema over the network, but the vendored copy
at `node/node_modules/resume-schema/schema.json` (v1.0.0) settles it:

| Object | `additionalProperties` |
|---|---|
| top level | **false** — do not add new top-level keys |
| `awards` items | **true** — extras allowed, so `links` is legal |
| `meta` | **true** — which is why `summaries` and `notes` already work |

Worth knowing: the `awards` item schema formally declares only `awarder`/`date`/`summary`/
`title`, so even the existing `url` passes only because extras are permitted. Caveat — that is
the vendored npm copy; `$schema` points at the master branch on GitHub, which may differ.

---

## Known, unfixed, not blocking

| Item | State |
|---|---|
| **Master is still 6 pages**, both locales | Trimming the summary freed ~⅓ page; the bullet split and the longer, better `work[2]` bullet consumed it again. Addressed for submissions by `mise run short` (**3 pages**, degrees preserved). **Shrinking the master is now off the table** — P8 was the lever and you have decided against merging, correctly: the blocks record real changes in focus. The master stays a 6-page archive and `mise run short` is the artifact to submit. |
| **The "nationwide" platform is unquantified — permanently** | `:85` both locales: "Maintained a nationwide production web platform while shipping new features against live traffic." The traffic, user and request-volume figures **do not exist / are not available**, so this cannot be fixed by rewriting. Originally classified as a *resume gap*; it is neither a resume nor a candidacy gap but a **missing-data gap**. The claim stays as written — "nationwide" is a factual statement of reach, defensible in an interview with "I don't have the traffic figures." Do not re-raise. |
| **Onboarding platform impact is not measurable yet** | Built and in testing; no production figures exist. The gain is expected to be both time (nine steps automated, plus tracking, notifications and update triggers that save staff effort) and operational quality — but none of it is measured, so **no number goes on the resume**; an estimate would be a fabricated result. The bullet now states capability instead. **Revisit once production data exists** — time per onboarding before → after is the figure to capture, and it would lift impact above 13/25. |
| **Terraform is a candidacy gap — do not add it** | You wrote Ansible scripts and Helm charts and used Kustomize, but have no recollection of Terraform, "at least not directly." So it stays off the resume entirely: claiming it would be the one thing a technical screen can trivially disprove. Ansible/Helm/Kustomize cover the same ground for most postings; if a JD names Terraform as a hard requirement, that is a genuine gap to weigh, not a wording problem. Do not re-raise. |
| **No leadership claim after 2022** | You held the technical-lead role on every project you were allocated to **until 2022**; the current role (2026) makes no leadership claim, and the resume correctly does not invent one. For a staff-level target this is a genuine gap in the *record*, not in the writing — nothing to fix here, but expect it as a screening question ("what does your leadership look like now?"). Related to **P13**, the seniority/title question. |
| **`Mentoring` is the one leadership keyword still unconfirmed** | `Mentoring` / `Mentoria` in Process & Leadership (en `:270`, pt `:260`) was never explicitly confirmed — you described the tech-lead role and code-review practice, not mentoring as such. Kept, because tech-leading 6–15 person teams for nine years without mentoring is implausible, and unlike OpenTelemetry it is an activity rather than a discrete tool you either used or did not. Drop it if you would rather not defend it. |
| **Separate blocks per phase — decided, do not re-raise** | The eight `work` entries stay as they are. Your title did not change but the way you worked and the technologies did, so each block records a distinct phase. **Correction to my earlier review:** I wrote that a scanner reading the same title twice "reads *padding*". That was overstated — same employer, same title, distinct date ranges is a normal and legible way to show a long tenure with phases, and each entry's `summary` already states the focus. My real concern was page count, which you have now settled. |
| **Past tense on the current role — decided, do not re-raise** | Kept as is. The role is ongoing but the projects inside it are finished, so "Built solo", "Shipped", "Delivered" each describe a completed deliverable rather than the role's status. That is the correct reading and it matches the convention documented in `SKILL.md`. Present tense would in fact be *less* accurate here, since it would imply the work is still in progress. |
| **Dissertation URL is now canonical** | `https://shorturl.at/p0ZhO` replaced with `https://repositorio.ufpe.br/handle/123456789/2601` in both locales — a UFPE institutional-repository handle, far more durable than a shortener and not stripped by parsers. **Not verified to load**: `repositorio.ufpe.br` is outside the network allowlist, so this is your resolution taken on trust. |
| **Two-column skills grid — accepted and documented** | The `pdf`/`html` skills grid interleaves under plain text extraction: proficiency levels detach from their categories and hyphenated keywords split (`Multi-arch builds` → `Multi-` / `arch builds`). Kept, because the grid is worth it for human readers and `txt`/`docx` are already single-column. Mitigation is artifact choice, not theme surgery. Now documented in `README.md` → **"Which format to submit"**, with the verification commands. Do not re-raise. |
| **Onboarding platform verb — settled as "automates"** | Still in testing, so the original "replacing a manual nine-step process" was overstated: it reads as an accomplished rollout. "**Automates**" is what ships, and it is accurate today. **Revisit once it is live** — at that point "replaces" becomes both accurate and stronger, and the production before/after timing becomes capturable at the same time. |
| **Three publications will never have a URL — closed** | Only KSACI has one (Springer chapter, verified). KEOPS, WJogos and the BCS-CMSG paper have no DOI, no index record, and you do not have the PDFs. Their **bibliographic records are now correct and complete** — titles, venues, page ranges, authorship position — which is what a reader can actually check. A citation without a link is normal for 2001–2008 workshop papers from small venues. Do not re-raise. |
| **Headline and titles — settled** | `basics.label` stays **"Senior Software Engineer"** while the work entries carry the official titles (`work[0]` = "Principal Technical Manager · Backend & Platform Engineering"). Headline = target role, entries = actual titles: a normal, ATS-friendly split. Consequence to accept: `basics.summary` opens "Senior backend engineer" and the four `meta.summaries` variants open with "engineer"/"engineering leader", which now agree with the headline rather than with `work[0]`. That is coherent under this choice. |
| **Pre-2009 titles are correct as written** | Entries 4–7 (2000-06 → 2009-01) keep Junior Software Engineer ×2, Software Configuration Management Engineer, Senior Software Configuration Management Engineer — confirmed as the real titles. Together with the 2009+ titles the progression reads Junior SWE → SCM Engineer → Senior SCM Engineer → Technical Manager → Senior Technical Manager → Principal Technical Manager. Do not re-raise. |
| **Skills render on page 4 of 6** in the master PDF | Follows from the page count. The short variant puts them on page 1. |
| **Section order differs between formats** | `md`/`txt`: Work → Education → Skills → Awards → Certifications → Publications → Languages. `pdf`/`html`: Experience → Skills → Education → Publications → Awards → Languages → Certificates. Neither is wrong, but "what a recruiter sees first" has to be tuned twice. Small change to unify if you want it. |

---

## Recommended order

1. **P6** — the last question needing a fact: which role(s) carry the Sentry work.
2. **P13** — the seniority/title call.
3. **P18** — optional; makes your reason for the separate blocks scannable.
4. **P15–P16** — publication record details; neither is blocking.
