"""PDF renderer — converts HTML to PDF using WeasyPrint."""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path


def _ensure_homebrew_lib_path() -> None:
    """Prepend Homebrew's lib directory to DYLD_LIBRARY_PATH on macOS.

    WeasyPrint's cffi bindings call dlopen() at import time.  On macOS with
    Homebrew, the GLib/Pango libraries live in /opt/homebrew/lib but that
    directory is not in the default dyld search path.  Setting
    DYLD_LIBRARY_PATH *before* the first dlopen() call (i.e. before
    `import weasyprint`) is enough because macOS's dlopen() re-reads the
    environment on every call — it is not cached at process startup.
    """
    if sys.platform != "darwin":
        return

    candidates = [
        "/opt/homebrew/lib",           # Apple Silicon
        "/usr/local/lib",              # Intel Homebrew
    ]
    key = "DYLD_LIBRARY_PATH"
    current_paths = [p for p in os.environ.get(key, "").split(":") if p]
    added = [p for p in candidates if os.path.isdir(p) and p not in current_paths]
    if added:
        os.environ[key] = ":".join(added + current_paths)


# Silence WeasyPrint's verbose font/CSS warnings; real errors still surface.
logging.getLogger("weasyprint").setLevel(logging.ERROR)
logging.getLogger("weasyprint.progress").setLevel(logging.ERROR)
logging.getLogger("fontTools").setLevel(logging.ERROR)


def render_pdf(html: str, output_path: Path) -> None:
    """Convert an HTML string to a PDF file at *output_path* using WeasyPrint.

    Raises ``ImportError`` if WeasyPrint is not installed and
    ``weasyprint.document.DocumentError`` (or similar) on render failure.
    """
    # Must run before `import weasyprint` triggers cffi's dlopen() calls.
    _ensure_homebrew_lib_path()

    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
    except ImportError as exc:
        raise ImportError(
            "WeasyPrint is required for PDF output.  "
            "Install it with:  uv add weasyprint  (or pip install weasyprint)"
        ) from exc

    font_config = FontConfiguration()

    print_css = CSS(
        string="""
        @page {
            size: A4;
            margin: 15mm 15mm 18mm 15mm;
        }
        body {
            font-size: 10pt;
        }
        a {
            color: inherit;
            text-decoration: none;
        }
        """,
        font_config=font_config,
    )

    HTML(string=html).write_pdf(
        output_path,
        stylesheets=[print_css],
        font_config=font_config,
        presentational_hints=True,
    )
