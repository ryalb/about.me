/**
 * render_theme.mjs — renders a JSON Resume using a jsonresume theme.
 *
 * Usage:
 *   bun render_theme.mjs <themeDir> <input.json> <output.html>
 *
 * <themeDir> is an absolute path to a theme package directory containing a
 * package.json.  Theme resolution (custom vs npm vs explicit path) and
 * on-demand installation are handled by the Python caller; this script only
 * loads and invokes the theme.
 *
 * Run with Bun — it transpiles JSX/TSX theme entry points natively, which
 * Node.js cannot do.
 */

import { createRequire } from "module";
import { readFileSync, writeFileSync, existsSync } from "fs";
import { resolve, basename } from "path";
import { pathToFileURL } from "url";

const require = createRequire(import.meta.url);

// ── Args ─────────────────────────────────────────────────────────────────
const [, , themeDir, inputFile, outputFile] = process.argv;

if (!themeDir || !inputFile || !outputFile) {
  console.error("Usage: bun render_theme.mjs <themeDir> <input.json> <output.html>");
  process.exit(1);
}

const pkgPath = resolve(themeDir, "package.json");
if (!existsSync(pkgPath)) {
  console.error(`[resume-generator] No package.json in theme directory: ${themeDir}`);
  process.exit(1);
}

// ── Load theme ────────────────────────────────────────────────────────────
const pkg = JSON.parse(readFileSync(pkgPath, "utf-8"));
const isESM = pkg.type === "module";

/** Pick an entry file from package.exports, falling back to package.main. */
function resolveEntry() {
  const mainExport = pkg.exports?.["."];

  if (typeof mainExport === "string") return mainExport;

  if (mainExport && typeof mainExport === "object") {
    const entry =
      mainExport.import?.default ??
      mainExport.import ??
      mainExport.default ??
      mainExport.require?.default ??
      mainExport.require;
    if (typeof entry === "string") return entry;
  }

  return pkg.main ?? "index.js";
}

let render;

try {
  if (isESM) {
    const entryPath = resolve(themeDir, resolveEntry());
    const mod = await import(pathToFileURL(entryPath).href);
    render = mod.render ?? mod.default?.render ?? mod.default;
  } else {
    const mod = require(resolve(themeDir, pkg.main ?? "index.js"));
    render = mod.render ?? mod.default?.render ?? mod;
  }
} catch (err) {
  console.error(`[resume-generator] Failed to load theme from ${themeDir}:`);
  console.error(err.stack ?? String(err));
  process.exit(1);
}

if (typeof render !== "function") {
  console.error(
    `[resume-generator] Theme '${basename(themeDir)}' does not export a render() function.`
  );
  process.exit(1);
}

// ── Render ────────────────────────────────────────────────────────────────
const resume = JSON.parse(readFileSync(inputFile, "utf-8"));
let html;

try {
  html = await render(resume, { pdfMode: false });
} catch {
  // Some themes accept no options argument.
  html = await render(resume);
}

writeFileSync(outputFile, html, "utf-8");
console.error(`[resume-generator] ✓ Rendered with theme: ${basename(themeDir)}`);
