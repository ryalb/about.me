"""
resume-generator — Generate polished resume versions from a master JSON Resume.

Usage examples:

  # Full resume, all formats, default theme
  resume generate resume.json

  # Specific theme, only recent 5 years, select sections
  resume generate resume.json \\
      --theme even \\
      --cut-date 2019-01-01 \\
      --sections work,education,skills,projects \\
      --formats html,pdf,md

  # Scale html/pdf/docx down to 90% to fit more on a page
  resume generate resume.json --zoom 90%

  # List available themes
  resume themes

  # List valid section names
  resume sections
"""

from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Annotated

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .filter import available_summaries, emptied_sections, filter_resume
from .models import ALL_SECTIONS
from .renderers.html import list_custom_themes, render_html
from .renderers.markdown import render_markdown
from .renderers.pdf import render_pdf
from .renderers.text import render_text
from .renderers.word import render_word

# ── App setup ────────────────────────────────────────────────────────────
app = typer.Typer(
    name="resume",
    help="Generate polished resume versions from a master JSON Resume file.",
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()

# ── Theme catalogue ───────────────────────────────────────────────────────
KNOWN_THEMES: dict[str, str] = {
    "even": "Clean, modern layout with icon accents (ESM)",
    "elegant": "Elegant two-column design",
    "paper": "Minimal, paper-like style",
    "flat": "Flat design with colour sections",
    "caffeine": "Bold, dark-accent modern layout",
    "classy": "Classic professional look",
    "spartan": "Ultra-minimal single-column",
    "kendall": "Material-design inspired",
    "actual": "Compact one-page format",
    "stackoverflow": "StackOverflow Developer Story style",
    "onepage": "Optimised single-page printing",
    "compact": "Space-efficient dense layout",
    "sceptile": "Green-accent clean theme",
    "straightforward": "No-frills straightforward layout",
}

ALL_FORMATS = ["html", "pdf", "md", "txt", "docx"]

# Zoom bounds, and the value at or above which a bare number is read as a
# percentage rather than a multiplier.
ZOOM_MIN = 0.5
ZOOM_MAX = 2.0
ZOOM_PERCENT_THRESHOLD = 10.0

# Formats whose layout is scalable; md and txt carry no sizing information.
ZOOMABLE_FORMATS = ("html", "pdf", "docx")


# ── Helpers ───────────────────────────────────────────────────────────────


def _parse_sections(raw: str | None) -> list[str] | None:
    if not raw:
        return None
    parts = [s.strip().lower() for s in raw.split(",") if s.strip()]
    invalid = [p for p in parts if p not in ALL_SECTIONS]
    if invalid:
        console.print(
            f"[red]Unknown section(s): {', '.join(invalid)}[/red]\n"
            f"Valid: {', '.join(ALL_SECTIONS)}"
        )
        raise typer.Exit(1)
    return parts


def _parse_cut_date(raw: str | None) -> date | None:
    if not raw:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=UTC).date()
        except ValueError:
            pass
    console.print(
        f"[red]Invalid cut-date '{raw}'. Expected YYYY-MM-DD, YYYY-MM, or YYYY.[/red]"
    )
    raise typer.Exit(1)


def _parse_formats(raw: str) -> list[str]:
    parts = [f.strip().lower().lstrip(".") for f in raw.split(",") if f.strip()]
    # Normalise aliases
    aliases = {"markdown": "md", "text": "txt", "word": "docx", "doc": "docx"}
    parts = [aliases.get(p, p) for p in parts]
    invalid = [p for p in parts if p not in ALL_FORMATS]
    if invalid:
        console.print(
            f"[red]Unknown format(s): {', '.join(invalid)}[/red]\n"
            f"Valid: {', '.join(ALL_FORMATS)}"
        )
        raise typer.Exit(1)
    return parts


def _parse_zoom(raw: str) -> float:
    """Parse a zoom level given as a multiplier (``1.1``) or percent (``110%``).

    A bare number of ``ZOOM_PERCENT_THRESHOLD`` or more is read as a percentage
    too, so ``--zoom 110`` and ``--zoom 110%`` agree.
    """
    text = raw.strip().rstrip("%").strip()
    try:
        value = float(text)
    except ValueError:
        console.print(
            f"[red]Invalid zoom '{raw}'. Expected a multiplier (1.1) "
            f"or a percentage (110%).[/red]"
        )
        raise typer.Exit(1)

    if raw.strip().endswith("%") or value >= ZOOM_PERCENT_THRESHOLD:
        value /= 100

    if not ZOOM_MIN <= value <= ZOOM_MAX:
        console.print(
            f"[red]Zoom {value:g} is out of range "
            f"({ZOOM_MIN:g}–{ZOOM_MAX:g}, i.e. {ZOOM_MIN:.0%}–{ZOOM_MAX:.0%}).[/red]"
        )
        raise typer.Exit(1)
    return value


def _output_folder(base_dir: Path, name: str | None) -> Path:
    today = datetime.now(UTC).date().strftime("%Y-%m-%d")
    folder_name = today if not name else f"{today}_{name}"
    folder = base_dir / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    return folder


# ── Commands ─────────────────────────────────────────────────────────────


@app.command()
def generate(
    resume_file: Annotated[
        Path,
        typer.Argument(
            help="Path to the master JSON Resume file.",
            exists=True,
            file_okay=True,
            readable=True,
        ),
    ],
    theme: Annotated[
        str,
        typer.Option(
            "--theme",
            "-t",
            help=(
                "Theme to render with. Defaults to the bundled "
                "[bold]base[/bold] custom theme (MDI icons, print-tuned). "
                "Resolution order: custom theme in "
                "[bold]custom/themes/[/bold], explicit directory path, then "
                "[bold]jsonresume-theme-*[/bold] npm package (installed on "
                "demand). Run [bold]resume themes[/bold] to list options."
            ),
            rich_help_panel="Content",
        ),
    ] = "base",
    sections: Annotated[
        str | None,
        typer.Option(
            "--sections",
            "-s",
            help=(
                "Comma-separated list of sections to include. "
                "Omit to include all. "
                "Run [bold]resume sections[/bold] to see valid names."
            ),
            rich_help_panel="Content",
        ),
    ] = None,
    cut_date: Annotated[
        str | None,
        typer.Option(
            "--cut-date",
            "-d",
            help=(
                "Exclude entries whose primary date is before this value. "
                "Format: YYYY-MM-DD, YYYY-MM, or YYYY. "
                "Ongoing roles (no endDate) are always kept."
            ),
            rich_help_panel="Content",
        ),
    ] = None,
    summary: Annotated[
        str | None,
        typer.Option(
            "--summary",
            "-S",
            help=(
                "Use a named summary variant from [bold]meta.summaries[/bold] "
                "instead of [bold]basics.summary[/bold]. "
                "Run [bold]resume summaries RESUME_FILE[/bold] to list them."
            ),
            rich_help_panel="Content",
        ),
    ] = None,
    no_summary: Annotated[
        bool,
        typer.Option(
            "--no-summary",
            help=(
                "Omit [bold]basics.summary[/bold] from every format — for "
                "variants that should open straight into the work history. "
                "Cannot be combined with [bold]--summary[/bold]."
            ),
            rich_help_panel="Content",
        ),
    ] = False,
    formats: Annotated[
        str,
        typer.Option(
            "--formats",
            "-f",
            help=f"Comma-separated output formats. Choices: {', '.join(ALL_FORMATS)}",
            rich_help_panel="Output",
        ),
    ] = ",".join(ALL_FORMATS),
    zoom: Annotated[
        str,
        typer.Option(
            "--zoom",
            "-z",
            help=(
                "Content scale for [bold]html[/bold], [bold]pdf[/bold] and "
                "[bold]docx[/bold], as a multiplier ([bold]1.15[/bold]) or a "
                "percentage ([bold]115%[/bold]). Type and spacing scale; page "
                "size and margins do not, so a higher zoom fits less on a "
                "page. md and txt are unaffected."
            ),
            rich_help_panel="Output",
        ),
    ] = "1.0",
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            "-o",
            help="Base output directory. A dated sub-folder is created automatically.",
            rich_help_panel="Output",
        ),
    ] = Path(".output"),
    name: Annotated[
        str | None,
        typer.Option(
            "--name",
            "-n",
            help="Optional label appended to the output folder name (e.g. 'frontend').",
            rich_help_panel="Output",
        ),
    ] = None,
    no_theme: Annotated[
        bool,
        typer.Option(
            "--no-theme",
            help="Skip Node.js theme rendering and use the built-in HTML template.",
            rich_help_panel="Output",
        ),
    ] = False,
    validate: Annotated[
        bool,
        typer.Option(
            "--validate/--no-validate",
            help="Validate the JSON against the official JSON Resume schema.",
            rich_help_panel="Content",
        ),
    ] = True,
) -> None:
    """Generate multiple resume formats from a master [bold]JSON Resume[/bold] file.

    Creates a dated folder under OUTPUT_DIR containing the requested
    output files.  The built-in HTML template is used as a fallback when
    Node.js or the requested theme is unavailable.
    """
    # ── Load & validate ───────────────────────────────────────────────────
    console.print(
        Panel.fit(
            f"[bold cyan]resume-generator[/bold cyan]  ·  {resume_file.name}",
            border_style="cyan",
        )
    )

    try:
        raw = json.loads(resume_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        console.print(f"[red]✗ Invalid JSON:[/red] {exc}")
        raise typer.Exit(1)

    if validate:
        _validate_schema(raw)

    # ── Parse options ─────────────────────────────────────────────────────
    selected_sections = _parse_sections(sections)
    cutoff = _parse_cut_date(cut_date)
    output_formats = _parse_formats(formats)
    zoom_factor = _parse_zoom(zoom)
    effective_theme = None if no_theme else theme

    if summary is not None and no_summary:
        console.print(
            "[red]--summary and --no-summary are mutually exclusive:[/red] "
            "one selects a summary, the other removes it."
        )
        raise typer.Exit(1)

    # ── Apply filters ─────────────────────────────────────────────────────
    try:
        filtered = filter_resume(
            raw, selected_sections, cutoff, summary, hide_summary=no_summary
        )
    except KeyError as exc:
        key, available = exc.args
        console.print(f"[red]Unknown summary variant '{key}'.[/red]")
        if available:
            console.print(f"Available: {', '.join(available)}")
        else:
            console.print(
                "[dim]No variants defined. Add a 'summaries' map under 'meta' "
                "in your resume file.[/dim]"
            )
        raise typer.Exit(1)

    if dropped := emptied_sections(raw, filtered):
        console.print(
            "[yellow]⚠ Filters removed every entry from:[/yellow] "
            f"{', '.join(dropped)}  [dim](section omitted from output)[/dim]"
        )

    # ── Summary ───────────────────────────────────────────────────────────
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    table.add_column(style="dim")
    table.add_column()
    table.add_row("Theme", effective_theme or "[dim](built-in)[/dim]")
    table.add_row("Sections", ", ".join(selected_sections or ALL_SECTIONS))
    table.add_row("Cut date", str(cutoff) if cutoff else "[dim]none[/dim]")
    table.add_row(
        "Summary",
        "[dim]hidden (--no-summary)[/dim]"
        if no_summary
        else (summary or "[dim]basics.summary[/dim]"),
    )
    table.add_row("Formats", ", ".join(output_formats))
    if zoom_factor != 1.0:
        scaled = [f for f in output_formats if f in ZOOMABLE_FORMATS]
        table.add_row(
            "Zoom",
            f"{zoom_factor:g}× ({zoom_factor:.0%})"
            + (
                f"  [dim]{', '.join(scaled)}[/dim]"
                if scaled
                else "  [dim](no effect on the selected formats)[/dim]"
            ),
        )
    console.print(table)

    # ── Output folder ─────────────────────────────────────────────────────
    out_dir = _output_folder(output_dir, name)
    console.print(f"[dim]Output → {out_dir}[/dim]\n")

    # ── Generate HTML (needed for both html + pdf) ────────────────────────
    html_content: str | None = None

    def _get_html() -> str:
        nonlocal html_content
        if html_content is None:
            html_content = render_html(
                filtered, effective_theme, zoom=zoom_factor, console=console
            )
        return html_content

    # ── Render each format ────────────────────────────────────────────────
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        results: list[tuple[str, Path, bool, str]] = []  # (fmt, path, ok, msg)

        for fmt in output_formats:
            task = progress.add_task(f"Generating [bold]{fmt}[/bold]…", total=None)

            try:
                out_file = _render_format(
                    fmt, filtered, _get_html, out_dir, zoom_factor
                )
                results.append((fmt, out_file, True, ""))
            except Exception as exc:  # noqa: BLE001 - one bad format must not abort the rest
                results.append((fmt, out_dir / f"resume.{fmt}", False, str(exc)))
            finally:
                progress.remove_task(task)

    # ── Print results ─────────────────────────────────────────────────────
    for fmt, path, ok, msg in results:
        rel = path.relative_to(Path.cwd()) if path.is_relative_to(Path.cwd()) else path
        if ok:
            console.print(f"  [green]✓[/green] [bold]{fmt:5}[/bold]  {rel}")
        else:
            console.print(f"  [red]✗[/red] [bold]{fmt:5}[/bold]  [dim]{msg}[/dim]")

    ok_count = sum(1 for _, _, ok, _ in results if ok)
    console.print(
        f"\n[bold green]{ok_count}/{len(results)}[/bold green] files generated in "
        f"[cyan]{out_dir}[/cyan]"
    )


def _render_format(
    fmt: str,
    resume: dict,
    get_html,
    out_dir: Path,
    zoom: float = 1.0,
) -> Path:
    """Render a single format and write the file. Returns the output path."""
    if fmt == "html":
        html = get_html()
        path = out_dir / "resume.html"
        path.write_text(html, encoding="utf-8")
        return path

    elif fmt == "pdf":
        html = get_html()
        path = out_dir / "resume.pdf"
        render_pdf(html, path, zoom=zoom)
        return path

    elif fmt == "md":
        md = render_markdown(resume)
        path = out_dir / "resume.md"
        path.write_text(md, encoding="utf-8")
        return path

    elif fmt == "txt":
        txt = render_text(resume)
        path = out_dir / "resume.txt"
        path.write_text(txt, encoding="utf-8")
        return path

    elif fmt == "docx":
        path = out_dir / "resume.docx"
        render_word(resume, path, zoom=zoom)
        return path

    else:
        raise ValueError(f"Unknown format: {fmt}")


def _validate_schema(resume: dict) -> None:
    """Validate against the official JSON Resume JSON Schema (offline-tolerant)."""
    try:
        import urllib.request

        import jsonschema

        schema_url = (
            "https://raw.githubusercontent.com/jsonresume/resume-schema"
            "/master/schema.json"
        )
        try:
            with urllib.request.urlopen(schema_url, timeout=5) as r:
                schema = json.loads(r.read())
            jsonschema.validate(resume, schema)
            console.print("[dim]✓ Schema validation passed[/dim]")
        except (OSError, TimeoutError):
            console.print("[dim]⚠ Schema validation skipped (no network)[/dim]")
        except jsonschema.ValidationError as exc:
            console.print(f"[yellow]⚠ Schema warning:[/yellow] {exc.message}")
    except ImportError:
        pass


# ── Informational commands ────────────────────────────────────────────────


@app.command()
def themes() -> None:
    """List available custom themes and known jsonresume npm themes."""
    custom = list_custom_themes()
    if custom:
        ctable = Table(
            title="Custom Themes (custom/themes/)",
            box=box.ROUNDED,
            header_style="bold magenta",
        )
        ctable.add_column("Theme", style="bold")
        ctable.add_column("Description")
        for name in custom:
            desc = ""
            pkg = Path("custom/themes") / name / "package.json"
            try:
                desc = json.loads(pkg.read_text()).get("description", "")
            except (OSError, json.JSONDecodeError):
                pass
            ctable.add_row(
                f"{name} [dim](default)[/dim]" if name == "base" else name,
                desc or "[dim]—[/dim]",
            )
        console.print(ctable)
        console.print(
            "[dim]Custom themes take precedence over npm packages "
            "with the same name.[/dim]\n"
        )

    table = Table(
        title="Known jsonresume Themes (npm)",
        box=box.ROUNDED,
        show_lines=False,
        header_style="bold cyan",
    )
    table.add_column("Theme", style="bold")
    table.add_column("Description")
    table.add_column("Install", style="dim")

    for theme_name, desc in KNOWN_THEMES.items():
        table.add_row(
            theme_name,
            desc,
            f"jsonresume-theme-{theme_name}",
        )

    console.print(table)
    console.print(
        "\n[dim]Any npm package matching [bold]jsonresume-theme-*[/bold] works — "
        "it will be installed automatically on first use.\n"
        "You can also pass a directory path directly, e.g. "
        "[bold]--theme ./custom/themes/base[/bold].[/dim]"
    )


@app.command()
def summaries(
    resume_file: Annotated[
        Path,
        typer.Argument(
            help="Path to the master JSON Resume file.",
            exists=True,
            file_okay=True,
            readable=True,
        ),
    ],
) -> None:
    """List the summary variants defined in [bold]meta.summaries[/bold]."""
    try:
        raw = json.loads(resume_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        console.print(f"[red]✗ Invalid JSON:[/red] {exc}")
        raise typer.Exit(1)

    variants = available_summaries(raw)
    if not variants:
        console.print(
            "[yellow]No summary variants defined.[/yellow]\n"
            "Add a [bold]summaries[/bold] map under [bold]meta[/bold]:\n\n"
            '  "meta": { "summaries": { "backend": "Senior backend engineer…" } }'
        )
        return

    default_summary = (raw.get("basics") or {}).get("summary", "")

    for key, text in variants.items():
        is_default = text.strip() == default_summary.strip()
        marker = "  [green](current basics.summary)[/green]" if is_default else ""
        console.print(f"\n[bold cyan]{key}[/bold cyan]{marker}")
        console.print(f"[dim]{len(text.split())} words[/dim]")
        console.print(text)

    console.print(
        f"\n[dim]Use with:[/dim] resume generate {resume_file.name} "
        f"--summary {next(iter(variants))}"
    )


@app.command()
def sections() -> None:
    """List all valid JSON Resume section names."""
    table = Table(
        title="JSON Resume Sections",
        box=box.ROUNDED,
        header_style="bold cyan",
    )
    table.add_column("Section", style="bold")
    table.add_column("Date field used for --cut-date")

    from .models import DATE_FIELD_MAP

    for sec in ALL_SECTIONS:
        date_field = DATE_FIELD_MAP.get(sec, "—")
        table.add_row(sec, date_field)

    console.print(table)


# ── Entry point ───────────────────────────────────────────────────────────


def main() -> None:
    app()


if __name__ == "__main__":
    main()
