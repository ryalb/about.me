import React from 'react';
import { renderResumeDocument } from '@jsonresume/core/ssr';
import Resume from './Resume.jsx';
import { fonts, colors } from './tokens.js';

export function render(resume) {
  return renderResumeDocument(<Resume resume={resume} />, {
    fonts: fonts.remote,
    headAfterStyles: `<style>
    /*
     * Bind the local font family across the weights the theme uses.
     * src: local() lets both browsers and WeasyPrint (via fontconfig)
     * pick the correct file per weight/style instead of synthesising
     * faux-bold or faux-italic from the regular face.
     */
    @font-face {
      font-family: 'IosevkaTermSlab Nerd Font Propo';
      font-weight: 300;
      font-style: normal;
      src: local('IosevkaTermSlab Nerd Font Propo Light'),
           local('IosevkaTermSlabNerdFontPropo-Light');
    }
    @font-face {
      font-family: 'IosevkaTermSlab Nerd Font Propo';
      font-weight: 400;
      font-style: normal;
      src: local('IosevkaTermSlab Nerd Font Propo'),
           local('IosevkaTermSlabNerdFontPropo-Regular');
    }
    @font-face {
      font-family: 'IosevkaTermSlab Nerd Font Propo';
      font-weight: 500;
      font-style: normal;
      src: local('IosevkaTermSlab Nerd Font Propo Medium'),
           local('IosevkaTermSlabNerdFontPropo-Medium');
    }
    @font-face {
      font-family: 'IosevkaTermSlab Nerd Font Propo';
      font-weight: 700;
      font-style: normal;
      src: local('IosevkaTermSlab Nerd Font Propo Bold'),
           local('IosevkaTermSlabNerdFontPropo-Bold');
    }
    @font-face {
      font-family: 'IosevkaTermSlab Nerd Font Propo';
      font-weight: 400;
      font-style: italic;
      src: local('IosevkaTermSlab Nerd Font Propo Italic'),
           local('IosevkaTermSlabNerdFontPropo-Italic');
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      margin: 0;
      padding: 0;
      background: ${colors.page};
      font-family: ${fonts.sans};
      /* Slab/mono faces render heavy at small sizes; smoothing helps. */
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      /* Disable Iosevka's default ligatures — unwanted in prose. */
      font-variant-ligatures: none;
      font-feature-settings: 'liga' 0, 'calt' 0;
    }
    @media print {
      body {
        background: ${colors.surface};
      }
      @page {
        size: A4;
        margin: 14mm 14mm 16mm 14mm;
      }
      /*
       * Entries are allowed to split across pages (see Item in Resume.jsx),
       * so guard against ugly splits: never leave or carry fewer than two
       * lines, and keep each bullet intact.
       */
      p, li {
        orphans: 3;
        widows: 3;
      }
      li {
        break-inside: avoid;
        page-break-inside: avoid;
      }
      a {
        color: inherit;
      }
    }
  </style>`,
    lang: 'en',
    dir: 'ltr',
    title: `${resume.basics?.name || 'Resume'} - Resume`,
    includeTokensCss: false,
  });
}

export default { render };
