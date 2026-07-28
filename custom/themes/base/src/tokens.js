/**
 * Design tokens for the `base` custom theme.
 *
 * Edit this file to restyle the theme — colours, type scale, spacing and
 * page geometry are all centralised here so `Resume.jsx` rarely needs
 * touching for visual changes.
 */

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
  name: '44px',
  sectionTitle: '12px',
  itemTitle: '17px',
  itemSubtitle: '14px',
  body: '14px',
  summary: '15px',
  meta: '13px',
  small: '12px',
};

export const space = {
  pagePaddingY: '64px',
  pagePaddingX: '48px',
  printPadding: '0',
  headerGap: '48px',
  sectionGap: '48px',
  itemGap: '24px',
};

export const layout = {
  maxWidth: '900px',
  // Tighten these two for a denser, more page-efficient PDF.
  printPagePaddingY: '0',
  printPagePaddingX: '0',
};
