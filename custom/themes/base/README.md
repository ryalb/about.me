# jsonresume-theme-base (custom)

Custom theme derived from [`jsonresume-theme-architects-portfolio`](https://www.npmjs.com/package/jsonresume-theme-architects-portfolio) — structural keylines and geometric precision, like a drafting sheet.

Intended as the **starting point for your own themes**: copy this folder, rename it, and it becomes available as `--theme <folder-name>` immediately.

## Usage

```bash
uv run resume generate resume.json --theme base
uv run resume generate resume.json --theme ./custom/themes/base   # explicit path
```

## Structure

| File | Purpose |
|---|---|
| `src/tokens.js` | **Edit this first.** Fonts, colours, type scale, spacing, page geometry. |
| `src/Resume.jsx` | Component tree and styled-components. |
| `src/index.jsx` | SSR entry — exports `render(resume)`, declares `@font-face` and `@page` rules. |
| `package.json` | Declares the `.` export pointing at `src/index.jsx`. |

Rendering is done by Bun, which transpiles JSX natively — there is **no build step**. Edit and re-run.

## Fonts

This theme uses **IosevkaTermSlab Nerd Font Propo** — a locally installed font, not a webfont.

```js
// src/tokens.js
export const fonts = {
  sans: "'IosevkaTermSlab Nerd Font Propo', 'IosevkaTermSlab Nerd Font', …",
  remote: [],   // no Google Fonts request
};
```

### How it resolves

| Output | Mechanism | Requirement |
|---|---|---|
| **PDF** | WeasyPrint → fontconfig → embeds a subset per weight | Font installed on the **generating** machine |
| **HTML** | Browser `@font-face src: local()` | Font installed on the **viewing** machine, else falls back |

Verify the font is visible to fontconfig:

```bash
fc-match "IosevkaTermSlab Nerd Font Propo"
# → IosevkaTermSlabNerdFontPropo-Regular.ttf: "IosevkaTermSlab Nerd Font Propo" "Regular"
```

Confirm the weights actually landed in a generated PDF:

```bash
python3 -c "
import re, zlib, sys
d = open('.output/YYYY-MM-DD/resume.pdf','rb').read()
out = set()
for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', d, re.S):
    try: dec = zlib.decompress(m.group(1))
    except Exception: continue
    out |= {f.decode().split('+')[-1] for f in re.findall(rb'/FontName\s*/([A-Za-z0-9+\-]+)', dec)}
print(*sorted(out), sep='\n')"
```

### Weights

The `@font-face` block in `src/index.jsx` binds each weight explicitly so neither the browser nor WeasyPrint synthesises faux-bold or faux-italic:

| CSS weight | Face | Used for |
|---|---|---|
| 300 | Light | Name, body copy, highlights |
| 400 | Regular | Item titles, contact line |
| 500 | Medium | Section titles, card titles |
| 700 | Bold | Available, currently unused |
| 400 italic | Italic | Available |

ExtraBold (800), Oblique and the Medium/Bold italics are installed and can be bound the same way if needed.

### Ligatures

Iosevka ships programming ligatures (`->`, `=>`, `!=`) which look wrong in prose. They're disabled globally:

```css
font-variant-ligatures: none;
font-feature-settings: 'liga' 0, 'calt' 0;
```

### Switching fonts

**To another local font** — change `fonts.sans` in `tokens.js` and update the `@font-face` family names and `local()` values in `src/index.jsx`.

**To a webfont** — put the URL in `fonts.remote` and delete the `@font-face` block:

```js
export const fonts = {
  sans: "'Inter', sans-serif",
  remote: ['https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap'],
};
```

Webfonts are more portable for shared HTML but require network access at PDF-generation time.

## Improvements over the upstream theme

The base theme silently dropped several JSON Resume fields. This version renders them:

| Field | Upstream | Here |
|---|---|---|
| `education.summary` | ✗ dropped | ✓ rendered (this is where dissertations live) |
| `education.courses` | ✗ dropped | ✓ rendered as a keyword row |
| `education.score` | ✗ dropped | ✓ appended to the degree line |
| `education.url` | ✗ dropped | ✓ institution is linked |
| `work.location` | ✗ dropped | ✓ shown next to company |
| `work.url` | ✗ dropped | ✓ company is linked |
| `skills.level` | ✗ dropped | ✓ shown right-aligned in card header |
| `certificates.url` | ✗ dropped | ✓ name is linked |
| `publications.url` | ✗ dropped | ✓ name is linked |
| `projects.keywords` | ✗ dropped | ✓ rendered as a keyword row |
| `projects.entity` / `roles` | ✗ dropped | ✓ shown in subtitle |
| `volunteer.url` | ✗ dropped | ✓ organization is linked |

Also changed:

- **Local font** — IosevkaTermSlab Nerd Font Propo replaces the Jost/Red Hat Display webfonts, with explicit per-weight `@font-face` bindings and ligatures disabled. No network request at render time.
- **Fixed the upstream page-break bug** — `@jsonresume/core`'s `<Section>` hard-codes `page-break-inside: avoid` on the whole `<section>`. For a section taller than one page (Experience, typically) that constraint is unsatisfiable, so the renderer pushes the entire section to the next page — leaving page 1 holding only the header and summary, and inflating the page count by ~25%. This theme overrides it back to `auto`. Any theme built on `@jsonresume/core`, including `architects-portfolio`, has this bug.
- **Granular print control instead** — sections and long entries may break internally; `ItemHeader` and individual bullets may not; `orphans: 3 / widows: 3` prevents stranded lines. Short atomic blocks (certificates, skill cards) still use `break-inside: avoid`.
- **A4 page rules** — explicit `@page { size: A4; margin: 14mm }`.
- **Awards and publications** get proper entry layout with right-aligned dates, rather than reusing the education block.
- **Certificates** use a compact variant, since they carry no body text.
- **Tokens extracted** to `src/tokens.js`.
- **Tighter vertical rhythm** — section gap 56px → 48px, name 48px → 44px, for better page efficiency.

## Customizing

Most visual changes only need `src/tokens.js`:

```js
export const colors = {
  ink: '#111827',      // headings
  accent: '#1f2937',   // links
  rule: '#d1d5db',     // keylines
  // …
};
```

For a denser PDF, reduce `space.sectionGap` and `space.itemGap`.

## Available `@jsonresume/core` helpers

`Section`, `DateRange`, `ContactInfo` are imported from `@jsonresume/core`. `renderResumeDocument` comes from `@jsonresume/core/ssr` and handles the HTML document shell, font links and styled-components stylesheet extraction.
