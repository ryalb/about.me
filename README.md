# resume-generator

Generate polished, multi-format resumes from a single master [JSON Resume](https://jsonresume.org) file. Apply any [jsonresume theme](https://jsonresume.org/themes), filter sections, and cut old entries — all from one CLI command.

```
resume generate resume.json --theme even --cut-date 2018 --sections work,education,skills
```

---

## Features

| Capability | Detail |
|---|---|
| **5 output formats** | HTML · PDF · Markdown · Plain text · Word (.docx) |
| **Theme support** | Any `jsonresume-theme-*` npm package, auto-installed on first use |
| **Custom themes** | Drop a theme folder in `custom/themes/` — no build step, JSX transpiled by Bun |
| **Built-in template** | Clean Jinja2 fallback — works without Bun |
| **Section filtering** | Include only the sections you need per variant |
| **Date cutoff** | Trim entries older than a given date; ongoing roles are always kept |
| **Summary variants** | Role-specific opening paragraphs selected with `--summary` |
| **Dated output folders** | Files land in `.output/YYYY-MM-DD[_name]/` automatically |
| **Schema validation** | Validates against the official JSON Resume JSON Schema |

---

## Requirements

| Dependency | Purpose |
|---|---|
| Python ≥ 3.11 | Runtime |
| [uv](https://docs.astral.sh/uv/) | Dependency & virtualenv management |
| [Bun](https://bun.sh) ≥ 1.0 | Theme installation & rendering (optional — built-in template used as fallback) |
| [WeasyPrint system libs](#weasyprint-system-libraries) | PDF generation |

---

## Installation

```bash
git clone <repo>
cd about.me
uv sync
```

> **macOS note:** uv's default cache directory may be blocked in some environments. If you see a cache error, run with `UV_CACHE_DIR=/tmp/uv-cache uv sync`.

Verify the install:

```bash
uv run resume --help
```

---

## Quick start

```bash
# Generate all formats with the default theme
uv run resume generate resume.json

# Targeted variant: custom theme, recent work only, role-specific summary
uv run resume generate resume.json \
    --theme base \
    --summary backend \
    --cut-date 2019-01-01 \
    --sections work,education,skills,projects \
    --formats html,pdf \
    --name "backend-role"
```

Output lands in `.output/YYYY-MM-DD/` (or `.output/YYYY-MM-DD_backend-role/`):

```
.output/
└── 2026-07-28_backend-role/
    ├── resume.html
    ├── resume.pdf
    ├── resume.md
    ├── resume.txt
    └── resume.docx
```

---

## Commands

### `resume generate`

```
resume generate [OPTIONS] RESUME_FILE
```

| Option | Short | Default | Description |
|---|---|---|---|
| `--theme` | `-t` | `even` | Custom theme name, directory path, or `jsonresume-theme-*` package name (prefix omitted). See [Themes](#themes). |
| `--sections` | `-s` | *(all)* | Comma-separated list of sections to include. |
| `--cut-date` | `-d` | *(none)* | Exclude entries whose primary date is before this value (`YYYY-MM-DD`, `YYYY-MM`, or `YYYY`). Ongoing roles (no `endDate`) are always kept. |
| `--summary` | `-S` | *(none)* | Use a named variant from `meta.summaries` instead of `basics.summary`. See [Summary variants](#summary-variants). |
| `--formats` | `-f` | `html,pdf,md,txt,docx` | Comma-separated output formats. |
| `--output-dir` | `-o` | `.output` | Base directory; a dated sub-folder is created automatically. |
| `--name` | `-n` | *(none)* | Label appended to the output folder name (e.g. `frontend`). |
| `--no-theme` | | `false` | Skip theme rendering; use the built-in HTML template. |
| `--no-validate` | | `false` | Skip JSON Schema validation. |

### `resume themes`

List custom themes (from `custom/themes/`) and known npm themes.

```bash
uv run resume themes
```

### `resume summaries`

List the summary variants defined in `meta.summaries`, with word counts. Marks which one currently matches `basics.summary`.

```bash
uv run resume summaries resume.json
```

### `resume sections`

List all valid section names and the date field used for `--cut-date` filtering.

```bash
uv run resume sections
```

---

## Themes

`--theme` accepts three kinds of reference, resolved in this order:

| # | Reference | Example | Resolves to |
|---|---|---|---|
| 1 | Directory path | `--theme ./custom/themes/base` | That directory |
| 2 | Custom theme name | `--theme base` | `custom/themes/base/` |
| 3 | npm package name | `--theme caffeine` | `jsonresume-theme-caffeine`, installed on demand |

Custom themes **shadow npm packages of the same name** — so you can fork `even` into `custom/themes/even/` and override it without touching `node_modules/`.

### npm themes

Any package published as `jsonresume-theme-*` works; pass the name without the prefix. It is installed into `node/node_modules/` on first use via `bun add`.

```bash
uv run resume generate resume.json --theme caffeine
uv run resume generate resume.json --theme architects-portfolio
```

Pre-bundled:

| Theme | Style |
|---|---|
| `even` | Clean modern layout with icon accents |
| `elegant` | Elegant two-column design |
| `paper` | Minimal paper-like style |
| `flat` | Flat design with colour sections |
| `caffeine` | Bold dark-accent modern layout |
| `architects-portfolio` | Drafting-sheet keylines (React/JSX) |

Run `uv run resume themes` for the full curated list.

### Custom themes

A custom theme is any folder under `custom/themes/` containing a `package.json` that exports a `render(resume)` function. It becomes available as `--theme <folder-name>` immediately — **no registration and no build step**, since Bun transpiles JSX/TSX natively.

The bundled `base` theme is a good starting point:

```
custom/themes/base/
├── src/tokens.js     # colours, type scale, spacing — edit this first
├── src/Resume.jsx    # component tree (styled-components)
├── src/index.jsx     # SSR entry: exports render(), sets fonts and @page rules
├── package.json      # declares the "." export → src/index.jsx
└── README.md
```

To create your own:

```bash
cp -r custom/themes/base custom/themes/mytheme
cd custom/themes/mytheme && BUN_INSTALL_CACHE_DIR=/tmp/bun-cache bun install
uv run resume generate resume.json --theme mytheme
```

Edit `src/tokens.js` for colours and spacing; edit `src/Resume.jsx` to change structure. Re-run to see changes.

See [`custom/themes/base/README.md`](custom/themes/base/README.md) for the full field-coverage table and customization notes.

**Built-in fallback:** if Bun is unavailable or the theme fails to render, the app falls back to a clean, print-ready built-in Jinja2 template and prints a warning. Use `--no-theme` to force it.

---

## Summary variants

Section filters change *what* appears; the opening summary changes *how you're positioned* — and it's usually the only paragraph a reviewer reads in full. Store role-specific versions under `meta.summaries` and select one at generation time.

```json
"meta": {
  "summaries": {
    "platform": "Software engineer with 25 years of unbroken ownership of build, release…",
    "backend":  "Senior backend engineer with 26 years building production systems…",
    "lead":     "Engineering leader with 26 years spanning hands-on delivery…",
    "ats":      "Senior software engineer with 26 years of experience across…"
  }
}
```

```bash
uv run resume summaries resume.json                              # list variants
uv run resume generate resume.json --summary lead --name mgmt    # apply one
uv run resume generate resume.json                               # basics.summary
```

With no `--summary` flag, `basics.summary` is used unchanged. `meta.summaries` is **always stripped from generated output**, so the variant map never leaks into a rendered resume.

An unknown key fails fast and lists what's available:

```
Unknown summary variant 'nope'.
Available: ats, backend, lead, platform
```

---

## Section filtering & date cutoff

### Section filtering

Pass a comma-separated list to `--sections` to include only those sections:

```bash
# Only work history, education, and skills
uv run resume generate resume.json --sections work,education,skills
```

Available sections: `basics`, `work`, `volunteer`, `education`, `awards`, `certificates`, `publications`, `skills`, `languages`, `interests`, `references`, `projects`.

`basics` is always included regardless of the section list.

### Date cutoff (`--cut-date`)

Removes entries whose primary date field is **before** the cutoff. The date field used per section:

| Section | Date field |
|---|---|
| `work`, `volunteer`, `education`, `projects` | `startDate` |
| `awards`, `certificates` | `date` |
| `publications` | `releaseDate` |

**Ongoing roles** (entries with a `startDate` but no `endDate`) are always kept even if `startDate` is before the cutoff — you're still in that role.

```bash
# Only positions started in the last ~7 years
uv run resume generate resume.json --cut-date 2018
```

---

## JSON Resume format

The input file must conform to the [JSON Resume schema](https://jsonresume.org/schema/). A minimal example:

```json
{
  "$schema": "https://raw.githubusercontent.com/jsonresume/resume-schema/master/schema.json",
  "basics": {
    "name": "Jane Doe",
    "label": "Software Engineer",
    "email": "jane@example.com",
    "phone": "+1 555 000 0000",
    "url": "https://janedoe.dev",
    "summary": "Full-stack engineer with 10 years of experience.",
    "location": { "city": "San Francisco", "region": "CA", "countryCode": "US" },
    "profiles": [
      { "network": "GitHub", "username": "janedoe", "url": "https://github.com/janedoe" },
      { "network": "LinkedIn", "username": "janedoe", "url": "https://linkedin.com/in/janedoe" }
    ]
  },
  "work": [
    {
      "name": "Acme Corp",
      "position": "Senior Engineer",
      "startDate": "2020-03",
      "summary": "Built and scaled core platform services.",
      "highlights": ["Reduced p99 latency by 40%", "Led migration to Kubernetes"]
    }
  ],
  "skills": [
    { "name": "Backend", "keywords": ["Python", "Go", "PostgreSQL"] }
  ]
}
```

The schema validator runs automatically (`--no-validate` to skip).

### Tooling extensions

The schema allows additional properties, so this project stores its own metadata inside the resume file:

| Key | Purpose |
|---|---|
| `meta.summaries` | Named summary variants for `--summary`. Stripped from output. |
| `work[].keywords` | Free-form tags for filtering when building role-specific versions. |

Both are ignored by standard JSON Resume tooling.

Two formatting rules matter in practice:

- **Omit fields rather than setting them empty.** `"endDate": ""` violates the schema's date pattern and makes themes render a dangling `2022-10 –`. Leaving `endDate` out is what signals "present".
- **Dates accept `YYYY`, `YYYY-MM` or `YYYY-MM-DD`.** Partial dates are fine and are compared correctly by `--cut-date`.

---

## WeasyPrint system libraries

WeasyPrint requires GLib, Pango, and Cairo native libraries for PDF rendering.

### macOS (Homebrew)

```bash
brew install pango cairo glib
```

The CLI automatically adds `/opt/homebrew/lib` to the dynamic linker path at runtime — no shell variable exports needed.

### Ubuntu / Debian

```bash
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libcairo2
```

### Other platforms

See the [WeasyPrint installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation).

---

## Project structure

```
about.me/
├── resume_generator/          # Python package
│   ├── main.py                # Typer CLI (generate / themes / summaries / sections)
│   ├── models.py              # Pydantic models for JSON Resume schema
│   ├── filter.py              # Section filtering, date cutoff, summary variants
│   └── renderers/
│       ├── html.py            # HTML — theme resolution + built-in Jinja2 template
│       ├── pdf.py             # PDF — WeasyPrint
│       ├── markdown.py        # Markdown renderer
│       ├── text.py            # Plain text renderer
│       └── word.py            # Word .docx — python-docx
├── custom/
│   └── themes/
│       └── base/              # Custom theme (React/JSX, no build step)
│           ├── src/tokens.js  # Design tokens — edit for restyling
│           ├── src/Resume.jsx # Component tree
│           └── src/index.jsx  # SSR entry
├── node/
│   ├── render_theme.mjs       # Bun script — loads & invokes a resolved theme dir
│   ├── package.json           # Bun manifest
│   ├── bun.lock               # Bun lockfile
│   └── node_modules/          # npm themes (even, elegant, paper, flat, caffeine…)
├── pyproject.toml
├── uv.lock
└── resume.json                # Your master resume
```

---

## Generating multiple resume variants

A common workflow is to maintain one master `resume.json` and generate tailored variants — combining `--sections`, `--cut-date` and `--summary`:

```bash
# Full resume — all sections, all formats
uv run resume generate resume.json --theme base --name full

# Engineering IC role — last 8 years, backend-focused summary
uv run resume generate resume.json \
    --name engineering \
    --theme base \
    --summary backend \
    --cut-date 2016 \
    --sections basics,work,education,skills,projects,certificates

# Management role — leadership summary, skip granular projects
uv run resume generate resume.json \
    --name management \
    --theme base \
    --summary lead \
    --sections basics,work,volunteer,education,awards,languages

# ATS submission — keyword-dense summary, Word output
uv run resume generate resume.json \
    --name ats \
    --summary ats \
    --formats docx,txt

# One-page PDF only — recent 5 years
uv run resume generate resume.json \
    --name onepage \
    --theme base \
    --cut-date 2021 \
    --formats pdf
```

Each run creates a new dated sub-folder so previous versions are never overwritten.
