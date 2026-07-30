/**
 * Design tokens for the `base` custom theme.
 *
 * Edit this file to restyle the theme — colours, type scale, spacing and
 * page geometry are all centralised here so `Resume.jsx` rarely needs
 * touching for visual changes.
 */

/**
 * Content zoom — a multiplier applied to every length the theme emits.
 *
 * `resume generate --zoom` passes the factor in through RESUME_ZOOM: a theme's
 * `render()` only receives the resume itself, so the environment is the one
 * channel available to the Python caller.  Unset or unparseable means 1.
 */
const zoom = (() => {
  const raw = Number.parseFloat(globalThis.process?.env?.RESUME_ZOOM ?? '');
  return Number.isFinite(raw) && raw > 0 ? raw : 1;
})();

/**
 * Scale a px length by the zoom factor.
 *
 * Sizes are emitted as pre-multiplied px rather than `calc()` over a CSS
 * variable so that the browser and WeasyPrint — which builds the PDF from this
 * same HTML — resolve every length identically.  Rounded to 2dp: enough
 * precision to keep the type scale smooth, short enough to keep the CSS terse.
 */
export const scale = (value) => `${Math.round(value * zoom * 100) / 100}px`;

export const colors = {
  ink: '#111827',        // headings, name
  body: '#374151',       // body copy
  muted: '#4b5563',      // secondary text, highlights
  subtle: '#6b7280',     // company names, labels
  faint: '#9ca3af',      // dates, separators
  rule: '#d1d5db',       // keylines under section titles
  hairline: '#e5e7eb',   // item separators
  surface: '#ffffff',    // card backgrounds
  page: '#fafaf9',       // page background (screen)
  accent: '#1f2937',     // links, emphasis
};

export const fonts = {
  /**
   * Primary family. Must be installed locally for PDF output — WeasyPrint
   * resolves it through fontconfig and embeds a subset in the PDF.
   * Verify availability with:  fc-match "IosevkaTermSlab Nerd Font Propo"
   *
   * The fallback chain degrades to other Iosevka variants, then to generic
   * slab/monospace faces, so HTML shared with machines lacking the font
   * still renders sensibly.
   */
  sans: "'IosevkaTermSlab Nerd Font Propo', 'IosevkaTermSlab Nerd Font', 'Iosevka Nerd Font Propo', 'Iosevka', 'Rockwell', 'Courier New', ui-monospace, monospace",

  /**
   * Remote webfonts to load. Empty because the primary family is local —
   * add a Google Fonts URL here if you switch to a hosted face.
   */
  remote: [],

  /**
   * Weights used by the theme. IosevkaTermSlab Nerd Font Propo ships
   * Light 300, Regular 400, Medium 500, Bold 700 and ExtraBold 800,
   * plus italic and oblique variants of each.
   */
  weights: {
    light: 300,
    regular: 400,
    medium: 500,
    bold: 700,
  },
};

export const type = {
  name: scale(44),
  sectionTitle: scale(12),
  itemTitle: scale(17),
  itemSubtitle: scale(14),
  body: scale(14),
  summary: scale(15),
  meta: scale(13),
  small: scale(12),
};

export const space = {
  pagePaddingY: scale(64),
  pagePaddingX: scale(48),
  printPadding: '0',
  headerGap: scale(48),
  sectionGap: scale(48),
  itemGap: scale(24),
};

export const layout = {
  // Scales with the zoom so the measure (characters per line) stays constant.
  maxWidth: scale(900),
  // Tighten these two for a denser, more page-efficient PDF.
  printPagePaddingY: '0',
  printPagePaddingX: '0',
};
