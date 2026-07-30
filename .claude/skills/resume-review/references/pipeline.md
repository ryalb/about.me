# Pipeline, verification and known engine limits

Facts below were verified in-session. Anything marked **verify** may have been fixed since —
check before relying on it.

## Who renders what

| Format | Code path | Notes |
| --- | --- | --- |
| `md` | `resume_generator/renderers/markdown.py` | |
| `txt` | `resume_generator/renderers/text.py` | 80-col wrap; ATS-safe |
| `docx` | `resume_generator/renderers/word.py` | python-docx; ATS-safe |
| `html` | `custom/themes/base/` (React + styled-components, run via Node/bun) | |
| `pdf` | that same HTML → WeasyPrint (`renderers/pdf.py`) | print CSS applies |
| `html` fallback | `renderers/html.py` Jinja template, only with `--no-theme` | keep in step with the theme |

**Consequence:** a label, field or layout fix usually needs the Python renderers *and* the
theme *and* the Jinja fallback. Fixing one and declaring victory is the standard failure
mode here. Grep all four.

## Commands

```bash
mise run build-all         # icons → clean → build both locales → copy to latest/ → check
mise run en                # en_US only (extra args pass through)
mise run pt                # pt_BR only
mise run check             # prek run --all-files  (run TWICE after a build)
mise run clean             # rm -rf .output

uv run resume generate resume-pt_br.json --theme base --name full_pt_br
uv run resume summaries resume-en_us.json     # list meta.summaries variants
uv run resume sections                        # valid --sections names
uv run resume themes
```

Useful `generate` flags: `--summary/-S <key>` (swap in a `meta.summaries` variant),
`--no-summary` (drop `basics.summary` entirely; not combinable with `--summary`),
`--sections/-s`, `--cut-date/-d` (ongoing roles are always kept), `--formats/-f`,
`--zoom/-z` (content scale for html/pdf/docx, `1.15` or `115%`, 50%–200%),
`--name/-n`, `--no-theme`, `--no-validate` (schema validation is on by default).

The `en` and `pt` tasks render at `--zoom 85%`, so page counts in `latest/` reflect that
scale rather than 100% — check `mise.toml` before reading a page count as a regression.

`mise run check` failing right after `build-all` with "files were modified by this hook" is
expected — the trailing-whitespace and EOF hooks rewrite the generated files. Re-run to
confirm green. A genuine failure to watch for: ruff `EXE001` ("shebang is present but file
is not executable") → `chmod +x <file>`.

## Verification

```bash
# PDF: page count and real laid-out text (catches layout, not just content)
pdfinfo latest/pt_br/resume.pdf | grep Pages
pdftotext -layout latest/en_us/resume.pdf - | grep -A16 '^SKILLS'
pdftotext -layout -f 8 -l 8 latest/pt_br/resume.pdf -   # inspect one page

# docx
unzip -p latest/pt_br/resume.docx word/document.xml | grep -o 'Presente'

# theme HTML: date ranges and grid rules
grep -o 'resume-date-range">[^<]*' latest/pt_br/resume.html | head
grep -o 'grid-template-columns:[^;}]*' latest/en_us/resume.html | sort -u
```

Prefer `pdftotext -layout` over reading the HTML when checking anything positional — it
shows what WeasyPrint actually produced. Two-column content appears as columns on one line.

## Locale parity check

Run this before and after content edits; the files drift.

```bash
python3 - <<'PY'
import json
en = json.load(open('resume-en_us.json'))
pt = json.load(open('resume-pt_br.json'))
for sec in ['work','education','awards','certificates','publications','skills','languages']:
    if len(en.get(sec,[])) != len(pt.get(sec,[])):
        print(f"COUNT {sec}: en={len(en.get(sec,[]))} pt={len(pt.get(sec,[]))}")
for i,(a,b) in enumerate(zip(en['work'], pt['work'])):
    for f in ['startDate','endDate']:
        if a.get(f) != b.get(f):
            print(f"work[{i}] {f}: en={a.get(f)!r} pt={b.get(f)!r}")
    ka, kb = a.get('keywords',[]), b.get('keywords',[])
    if ka != kb:
        print(f"work[{i}] keywords en-only={[k for k in ka if k not in kb]} pt-only={[k for k in kb if k not in ka]}")
for a,b in zip(en['skills'], pt['skills']):
    ka, kb = a.get('keywords',[]), b.get('keywords',[])
    extra = [k for k in ka if k not in kb], [k for k in kb if k not in ka]
    if extra[0] or extra[1]:
        print(f"skills {a['name']}: en-only={extra[0]} pt-only={extra[1]}")
PY
```

Translated keywords show up as differences on both sides — that's expected noise. A term
present on one side only (no counterpart) is a real gap.

## Engine limits and data semantics

**WeasyPrint 69 does not resolve `repeat(auto-fill, …)` / `auto-fit` into a track count.**
Every grid item lands in one full-width column in the PDF while the browser shows several.
Explicit track lists (`repeat(2, minmax(0, 1fr))`, `1fr 1fr`) work. `CardGrid` in
`custom/themes/base/src/Resume.jsx` carries a `@media print` override for exactly this.
Generalize the lesson: **any CSS layout change must be checked in the PDF**, not the HTML.

**Ongoing roles: omit `endDate`.** Do not write `"endDate": "present"` — the schema wants an
ISO date, and the literal renders lowercase and inconsistent. `@jsonresume/utils`
distinguishes *undefined* `endDate` (a single point in time — award/certificate dates) from
explicit `null` (the ongoing sentinel that gets the "Present" label), so the theme passes
`endDate ?? null` for every date **range** (work, education, projects, volunteer). If you
add another range section, pass `?? null` there too or the marker silently disappears.

**`meta.language`** (BCP 47: `en-US`, `pt-BR`) drives the ongoing-role label. Two tables
must stay in step:
- `resume_generator/i18n.py` → `present_label()`, used by md/txt/docx and the Jinja fallback
- `PRESENT_LABELS` in `custom/themes/base/src/Resume.jsx`, used by html/pdf

The label is passed as `presentLabel`, deliberately **not** via `DateRange`'s `locale` prop —
`locale` would also localize month names and rewrite every date in the document.

**`meta.summaries`** holds role-targeted opening paragraphs (`platform`, `backend`, `lead`,
`ats`) selected with `--summary <key>`; `filter.py:strip_summary_map` keeps the map out of
generated output. When `basics.summary` is rewritten, these go stale — check them.

**Renderers ignore unknown fields.** `certificates` uses only
`name`/`date`/`issuer`/`url`; `Certificate` in `models.py` allows extras but nothing renders
them.

## Known gaps (verify — may be fixed)

- **Section titles are hardcoded English in every renderer**, so pt_BR output shows
  `SKILLS`, `CERTIFICATIONS`, `AWARDS`. Fixing this means a label table per renderer plus
  the theme, keyed off `meta.language` like `present_label`.
- **pt_BR runs one page longer than en_US** (Portuguese is ~20–25% longer). Levers:
  condense pt_BR prose, or `space.sectionGap`/`itemGap` in
  `custom/themes/base/src/tokens.js` — the latter changes both locales and the design, so
  ask first.
- **`C` appears in pt_BR's Backend skill keywords but not en_US's**, though both work
  histories cite a C telephony platform.
- **Decaying claims:** "26 years" (earliest `startDate` is 2000-06) and "top 2026
  contributor" appear in `basics.summary` and several `meta.summaries` variants.
