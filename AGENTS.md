# AGENTS.md — about.me (resume-generator)

## Source of truth

- Master resumes live in `src/`:
  - `src/ryan-resume-en_us.json` — en-US master (edit here first)
  - `src/ryan-resume-pt_br.json` — pt-BR translation
  - `src/sheyla-resume-pt_br.json` — pt-BR academic CV (different section set + zoom)
- `latest/en_us/` and `latest/pt_br/` are committed rendered artifacts. Regenerate via `mise run build-all`, never edit by hand.
- The Python package is `resume_generator/`. The CLI entrypoint is `resume_generator.main:app` (`resume` console script).

## Commands

Always run inside the repo root. `uv` owns `.venv`; `mise` only pins tools.

```bash
mise install          # install pinned tools (python, uv, bun, ruff, prek)
mise run setup        # uv sync + prek install (first-time setup)
```

Build / check:
```bash
mise run build        # docker compose en + pt + sheyla-pt
mise run build-all    # icons → clean → build → copy to latest/ → fmt → check
mise run short        # condensed portal variants (ats summary, cut 2013, no highlights)
mise run short-all    # short + fmt + check
mise run lint         # ruff check resume_generator
mise run fmt          # ruff format resume_generator
mise run typecheck    # ty check
mise run check        # prek run --all-files (trailing-ws, EOF, ruff, ty, json, toml, etc.)
mise run icons        # python scripts/fetch_icons.py (refresh MDI icon subset)
mise run clean        # rm -rf .output
```

Single resume:
```bash
uv run resume generate src/ryan-resume-en_us.json --theme base --name full --zoom 80% --locale en-US
docker compose run --rm --build en    # same, inside Docker
```

Tests:
```bash
uv run pytest                         # all tests
uv run pytest tests/test_i18n.py      # single file
```

Order matters: `build-all` runs `fmt` then `check`. `check` must pass before committing — generated text is already normalized (see `_normalize_text` in `main.py`), so a `check` failure is a real regression, not a formatting artifact.

## Architecture

```
src/                    → master JSON Resume files (one per locale/person)
latest/                 → committed rendered outputs per locale
resume_generator/       → Python package
  main.py               → Typer CLI (generate / themes / summaries / sections)
  i18n.py               → locale resolution & label tables
  filter.py             → section filtering, --cut-date, --summary, --no-highlights
  icons.py              → vendored MDI SVG icons
  renderers/
    html.py             → Node.js theme rendering (bun) with built-in Jinja2 fallback
    pdf.py              → WeasyPrint from the rendered HTML
    markdown.py         → md
    text.py             → txt
    word.py             → docx (python-docx)
custom/themes/base/     → default React/JSX theme (Bun transpiles, no build step)
  src/tokens.js         → design tokens + scale() for --zoom
  src/Resume.jsx        → component tree + MDI contact line
  locales/              → JSX theme label tables (must stay in sync with resume_generator/locales/)
node/
  render_theme.mjs      → Bun SSR entry that loads a resolved theme dir
  node_modules/         → npm jsonresume themes (even, elegant, paper, flat, caffeine…)
resume_generator/locales/ → Python renderer label tables (en.json, pt.json)
```

## Conventions & gotchas

- **Locale tables must stay in sync**: Python (`resume_generator/locales/`) and JSX (`custom/themes/base/locales/`) both ship `en.json` and `pt.json`. Any new label key must be added to both. `tests/test_i18n.py` enforces this — if you add a key, run `uv run pytest` before committing.
- **`--locale` overrides `meta.language`**: The Compose services pass `--locale` explicitly so `latest/` is reproducible. When generating manually, pass `--locale` if you want labels to match the source file's language.
- **`--cut-date` exempts `education`**: Degrees are dated by `startDate`; a cutoff would silently drop them. Use `--sections` to drop education deliberately.
- **`--no-highlights` only affects `work`**: `projects` and `volunteer` highlights are left alone by design.
- **Skills are two-column cards in HTML/PDF**: Intentional ATS tradeoff. Use `txt` or `docx` for strict ATS portals.
- **Zoom reaches the `base` theme via `RESUME_ZOOM` env var**: Third-party npm themes ignore `--zoom`. Custom themes must import `scale()` from `tokens.js`.
- **Binary files in `latest/`**: `resume.pdf` and `resume.docx` change size even when content is byte-identical. `git diff` on these is noise; trust the build.
- **Docker volume quirk**: `compose.yaml` mounts `./src:/app/src.:ro` (note the trailing dot). Do not remove it; it is intentional and required by the Dockerfile `COPY src ./src` path resolution.
- **`sheyla-pt` is a different shape**: Reduced sections (`basics,interests,work,education,certificates,publications,awards`) and 70% zoom. Do not copy its settings to `en`/`pt` without adjusting `compose.yaml` and `mise.toml`.
- **No CI configured**: There are no GitHub Actions workflows. Verification is local only (`mise run check`).
- **`prek` runs on commit**: Git hooks from `prek.toml` run automatically. If you see a hook failure, fix it before amending; the hook will not run again on `git commit --amend` unless you re-stage.
