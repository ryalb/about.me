"""HTML renderer — uses jsonresume Node.js themes with a built-in Jinja2 fallback."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from jinja2 import BaseLoader, Environment

from ..icons import icon_svg

# ---------------------------------------------------------------------------
# Node.js theme rendering
# ---------------------------------------------------------------------------

# Path to the Node.js render script (sibling of this package)
_PROJECT_ROOT = Path(__file__).parents[2]
_NODE_SCRIPT = _PROJECT_ROOT / "node" / "render_theme.mjs"
_NODE_MODULES = _PROJECT_ROOT / "node" / "node_modules"
_CUSTOM_THEMES = _PROJECT_ROOT / "custom" / "themes"


def list_custom_themes() -> list[str]:
    """Return the names of custom themes found under ``custom/themes/``."""
    if not _CUSTOM_THEMES.is_dir():
        return []
    return sorted(
        d.name
        for d in _CUSTOM_THEMES.iterdir()
        if d.is_dir() and (d / "package.json").is_file()
    )


def resolve_theme(theme: str) -> tuple[Path, str]:
    """Resolve a theme reference to a directory on disk.

    Resolution order:
      1. Explicit filesystem path (contains a separator or starts with '.')
      2. Custom theme in ``custom/themes/<theme>/``
      3. Installed npm package ``node/node_modules/jsonresume-theme-<theme>``
      4. Install the npm package with ``bun add``, then use it

    Returns ``(theme_dir, origin)`` where *origin* is one of
    ``"path"``, ``"custom"`` or ``"npm"``.
    """
    # 1. Explicit filesystem path
    if "/" in theme or "\\" in theme or theme.startswith("."):
        candidate = Path(theme).expanduser().resolve()
        if not (candidate / "package.json").is_file():
            raise RuntimeError(f"No package.json found in theme directory: {candidate}")
        return candidate, "path"

    # 2. Custom theme
    custom = _CUSTOM_THEMES / theme
    if (custom / "package.json").is_file():
        return custom.resolve(), "custom"

    # 3./4. npm package, installed on demand
    pkg = _NODE_MODULES / f"jsonresume-theme-{theme}"
    if not (pkg / "package.json").is_file():
        _install_theme(theme)
    if not (pkg / "package.json").is_file():
        raise RuntimeError(f"Theme 'jsonresume-theme-{theme}' could not be installed.")
    return pkg.resolve(), "npm"


def render_with_theme(resume: dict[str, Any], theme: str) -> str:
    """Render HTML using a jsonresume theme via Bun.

    Accepts a custom theme name (``custom/themes/<name>/``), an explicit
    filesystem path, or an npm package name (installed on demand with
    ``bun add``).  Runs the render script with Bun, which supports
    JSX/TSX natively.

    Raises RuntimeError if Bun is unavailable or rendering fails.
    """
    bun_bin = _find_bun()
    if not bun_bin:
        raise RuntimeError(
            "Bun not found — cannot render with theme. Install from https://bun.sh"
        )

    theme_dir, _origin = resolve_theme(theme)

    with (
        tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as jf,
        tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as hf,
    ):
        json.dump(resume, jf)
        jf.flush()
        html_path = Path(hf.name)

    result = subprocess.run(
        [bun_bin, str(_NODE_SCRIPT), str(theme_dir), jf.name, hf.name],
        capture_output=True,
        text=True,
        check=False,
    )
    Path(jf.name).unlink(missing_ok=True)

    if result.returncode != 0:
        raise RuntimeError(f"Theme rendering failed:\n{result.stderr.strip()}")

    html = html_path.read_text(encoding="utf-8")
    html_path.unlink(missing_ok=True)
    return html


def _find_bun() -> str | None:
    try:
        r = subprocess.run(["bun", "--version"], capture_output=True, check=False)
        if r.returncode == 0:
            return "bun"
    except FileNotFoundError:
        pass
    return None


def _install_theme(theme: str) -> None:
    node_dir = _NODE_MODULES.parent
    bun_bin = _find_bun()
    if not bun_bin:
        raise RuntimeError(
            "Bun not found — cannot install theme. Install from https://bun.sh"
        )
    env = {**os.environ, "BUN_INSTALL_CACHE_DIR": "/tmp/bun-cache"}
    subprocess.run(
        [bun_bin, "add", f"jsonresume-theme-{theme}"],
        cwd=str(node_dir),
        env=env,
        check=True,
    )


# ---------------------------------------------------------------------------
# Built-in Jinja2 fallback template
# ---------------------------------------------------------------------------

_BUILTIN_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{ name }}</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --accent: #2563eb;
      --text: #1e293b;
      --muted: #64748b;
      --border: #e2e8f0;
      --bg: #ffffff;
    }
    body { font-family: 'Segoe UI', system-ui, sans-serif; color: var(--text);
           background: var(--bg); max-width: 860px; margin: 2rem auto; padding: 0 1.5rem; }
    a { color: var(--accent); text-decoration: none; }
    a:hover { text-decoration: underline; }

    /* Header */
    header { border-bottom: 2px solid var(--accent); padding-bottom: 1.25rem; margin-bottom: 1.75rem; }
    header h1 { font-size: 2rem; font-weight: 700; letter-spacing: -.5px; }
    header .label { font-size: 1.1rem; color: var(--accent); font-weight: 500; margin: .2rem 0 .6rem; }
    header .contact { display: flex; flex-wrap: wrap; gap: .4rem 1.2rem; font-size: .875rem; color: var(--muted); }
    header .contact span { display: inline-flex; align-items: center; gap: .3rem; }
    /* Inline MDI (Iconify) icons inherit text colour via fill="currentColor" */
    .icon { flex: none; vertical-align: -.125em; }

    /* Sections */
    section { margin-bottom: 1.75rem; }
    h2 { font-size: 1.1rem; font-weight: 600; text-transform: uppercase;
         letter-spacing: .08em; color: var(--accent); border-bottom: 1px solid var(--border);
         padding-bottom: .3rem; margin-bottom: 1rem; }
    .summary { line-height: 1.65; color: var(--muted); }

    /* Entry */
    .entry { margin-bottom: 1.25rem; }
    .entry-header { display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: .25rem; }
    .entry-title { font-weight: 600; font-size: 1rem; }
    .entry-subtitle { color: var(--muted); font-size: .9rem; }
    .entry-date { font-size: .82rem; color: var(--muted); white-space: nowrap; }
    .entry-body { margin-top: .4rem; font-size: .9rem; line-height: 1.6; color: #334155; }
    ul.highlights { margin: .4rem 0 0 1.1rem; }
    ul.highlights li { margin-bottom: .2rem; font-size: .875rem; }

    /* Skills */
    .skills-grid { display: flex; flex-wrap: wrap; gap: .5rem; }
    .skill-tag { background: #f1f5f9; border: 1px solid var(--border); border-radius: 4px;
                 padding: .15rem .55rem; font-size: .82rem; }

    /* Print */
    @media print {
      body { margin: 0; padding: 0; max-width: none; }
    }
  </style>
</head>
<body>

{% if basics %}
<header>
  <h1>{{ basics.name or '' }}</h1>
  {% if basics.label %}<div class="label">{{ basics.label }}</div>{% endif %}
  <div class="contact">
    {% if basics.email %}<span>{{ icon('email') }}<a href="mailto:{{ basics.email }}">{{ basics.email }}</a></span>{% endif %}
    {% if basics.phone %}<span>{{ icon('phone') }}{{ basics.phone }}</span>{% endif %}
    {% if basics.url %}<span>{{ icon('website') }}<a href="{{ basics.url }}">{{ basics.url }}</a></span>{% endif %}
    {% if basics.location %}
      {% set loc = basics.location %}
      <span>{{ icon('location') }}{{ [loc.city, loc.region, loc.countryCode] | select | join(', ') }}</span>
    {% endif %}
    {% for p in basics.profiles or [] %}
      <span>{{ icon(p.network | lower if p.network else 'website') }}{% if p.network %}{{ p.network }}: {% endif %}<a href="{{ p.url or '#' }}">{{ p.username or p.url }}</a></span>
    {% endfor %}
  </div>
</header>
{% if basics.summary %}
<section>
  <h2>Summary</h2>
  <p class="summary">{{ basics.summary }}</p>
</section>
{% endif %}
{% endif %}

{% macro date_range(start, end) %}
  {%- if start or end -%}
    {{ start or '' }}{% if end %} – {{ end }}{% elif start %} – Present{% endif %}
  {%- endif -%}
{% endmacro %}

{% if work %}
<section>
  <h2>Work Experience</h2>
  {% for job in work %}
  <div class="entry">
    <div class="entry-header">
      <div>
        <span class="entry-title">{{ job.position or '' }}</span>
        {% if job.name %} — <a href="{{ job.url or '#' }}">{{ job.name }}</a>{% endif %}
        {% if job.location %}<span class="entry-subtitle"> · {{ job.location }}</span>{% endif %}
      </div>
      <span class="entry-date">{{ date_range(job.startDate, job.endDate) }}</span>
    </div>
    {% if job.summary %}<div class="entry-body">{{ job.summary }}</div>{% endif %}
    {% if job.highlights %}
    <ul class="highlights">
      {% for h in job.highlights %}<li>{{ h }}</li>{% endfor %}
    </ul>
    {% endif %}
  </div>
  {% endfor %}
</section>
{% endif %}

{% if education %}
<section>
  <h2>Education</h2>
  {% for edu in education %}
  <div class="entry">
    <div class="entry-header">
      <div>
        <span class="entry-title">{{ edu.studyType or '' }}{% if edu.area %} in {{ edu.area }}{% endif %}</span>
        {% if edu.institution %} — {{ edu.institution }}{% endif %}
      </div>
      <span class="entry-date">{{ date_range(edu.startDate, edu.endDate) }}</span>
    </div>
    {% if edu.score %}<div class="entry-subtitle">Score: {{ edu.score }}</div>{% endif %}
    {% if edu.courses %}
    <ul class="highlights">
      {% for c in edu.courses %}<li>{{ c }}</li>{% endfor %}
    </ul>
    {% endif %}
  </div>
  {% endfor %}
</section>
{% endif %}

{% if skills %}
<section>
  <h2>Skills</h2>
  {% for skill in skills %}
  <div class="entry" style="margin-bottom:.75rem">
    <strong>{{ skill.name }}</strong>{% if skill.level %} <span class="entry-subtitle">({{ skill.level }})</span>{% endif %}
    {% if skill.keywords %}
    <div class="skills-grid" style="margin-top:.4rem">
      {% for kw in skill.keywords %}<span class="skill-tag">{{ kw }}</span>{% endfor %}
    </div>
    {% endif %}
  </div>
  {% endfor %}
</section>
{% endif %}

{% if projects %}
<section>
  <h2>Projects</h2>
  {% for proj in projects %}
  <div class="entry">
    <div class="entry-header">
      <div>
        <span class="entry-title">{% if proj.url %}<a href="{{ proj.url }}">{{ proj.name }}</a>{% else %}{{ proj.name }}{% endif %}</span>
        {% if proj.type %}<span class="entry-subtitle"> · {{ proj.type }}</span>{% endif %}
      </div>
      <span class="entry-date">{{ date_range(proj.startDate, proj.endDate) }}</span>
    </div>
    {% if proj.description %}<div class="entry-body">{{ proj.description }}</div>{% endif %}
    {% if proj.keywords %}
    <div class="skills-grid" style="margin-top:.4rem">
      {% for kw in proj.keywords %}<span class="skill-tag">{{ kw }}</span>{% endfor %}
    </div>
    {% endif %}
    {% if proj.highlights %}
    <ul class="highlights">
      {% for h in proj.highlights %}<li>{{ h }}</li>{% endfor %}
    </ul>
    {% endif %}
  </div>
  {% endfor %}
</section>
{% endif %}

{% if volunteer %}
<section>
  <h2>Volunteer</h2>
  {% for v in volunteer %}
  <div class="entry">
    <div class="entry-header">
      <div>
        <span class="entry-title">{{ v.position or '' }}</span>
        {% if v.organization %} — {{ v.organization }}{% endif %}
      </div>
      <span class="entry-date">{{ date_range(v.startDate, v.endDate) }}</span>
    </div>
    {% if v.summary %}<div class="entry-body">{{ v.summary }}</div>{% endif %}
    {% if v.highlights %}
    <ul class="highlights">{% for h in v.highlights %}<li>{{ h }}</li>{% endfor %}</ul>
    {% endif %}
  </div>
  {% endfor %}
</section>
{% endif %}

{% if awards %}
<section>
  <h2>Awards</h2>
  {% for a in awards %}
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">{% if a.url %}<a href="{{ a.url }}">{{ a.title }}</a>{% else %}{{ a.title }}{% endif %}</span>
      <span class="entry-date">{{ a.date or '' }}</span>
    </div>
    {% if a.awarder %}<div class="entry-subtitle">{{ a.awarder }}</div>{% endif %}
    {% if a.summary %}<div class="entry-body">{{ a.summary }}</div>{% endif %}
  </div>
  {% endfor %}
</section>
{% endif %}

{% if certificates %}
<section>
  <h2>Certifications</h2>
  {% for c in certificates %}
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">{% if c.url %}<a href="{{ c.url }}">{{ c.name }}</a>{% else %}{{ c.name }}{% endif %}</span>
      <span class="entry-date">{{ c.date or '' }}</span>
    </div>
    {% if c.issuer %}<div class="entry-subtitle">{{ c.issuer }}</div>{% endif %}
  </div>
  {% endfor %}
</section>
{% endif %}

{% if publications %}
<section>
  <h2>Publications</h2>
  {% for pub in publications %}
  <div class="entry">
    <div class="entry-header">
      <span class="entry-title">{% if pub.url %}<a href="{{ pub.url }}">{{ pub.name }}</a>{% else %}{{ pub.name }}{% endif %}</span>
      <span class="entry-date">{{ pub.releaseDate or '' }}</span>
    </div>
    {% if pub.publisher %}<div class="entry-subtitle">{{ pub.publisher }}</div>{% endif %}
    {% if pub.summary %}<div class="entry-body">{{ pub.summary }}</div>{% endif %}
  </div>
  {% endfor %}
</section>
{% endif %}

{% if languages %}
<section>
  <h2>Languages</h2>
  <div class="skills-grid">
    {% for lang in languages %}
    <span class="skill-tag"><strong>{{ lang.language }}</strong>{% if lang.fluency %} · {{ lang.fluency }}{% endif %}</span>
    {% endfor %}
  </div>
</section>
{% endif %}

{% if interests %}
<section>
  <h2>Interests</h2>
  {% for interest in interests %}
  <div style="margin-bottom:.5rem">
    <strong>{{ interest.name }}</strong>
    {% if interest.keywords %}
    <div class="skills-grid" style="margin-top:.3rem">
      {% for kw in interest.keywords %}<span class="skill-tag">{{ kw }}</span>{% endfor %}
    </div>
    {% endif %}
  </div>
  {% endfor %}
</section>
{% endif %}

{% if references %}
<section>
  <h2>References</h2>
  {% for ref in references %}
  <div class="entry">
    <div class="entry-title">{{ ref.name }}</div>
    <div class="entry-body"><em>{{ ref.reference }}</em></div>
  </div>
  {% endfor %}
</section>
{% endif %}

</body>
</html>
"""


def render_builtin(resume: dict[str, Any]) -> str:
    """Render HTML using the built-in Jinja2 template (no Node.js required)."""
    env = Environment(loader=BaseLoader(), autoescape=False)
    env.filters["select"] = lambda seq: [x for x in seq if x]
    tmpl = env.from_string(_BUILTIN_TEMPLATE)

    basics = resume.get("basics", {}) or {}
    name = basics.get("name", "Resume")

    return tmpl.render(
        icon=icon_svg,
        name=name,
        basics=basics,
        work=resume.get("work", []),
        volunteer=resume.get("volunteer", []),
        education=resume.get("education", []),
        awards=resume.get("awards", []),
        certificates=resume.get("certificates", []),
        publications=resume.get("publications", []),
        skills=resume.get("skills", []),
        languages=resume.get("languages", []),
        interests=resume.get("interests", []),
        references=resume.get("references", []),
        projects=resume.get("projects", []),
    )


def render_html(
    resume: dict[str, Any],
    theme: str | None,
    console=None,
) -> str:
    """Render HTML, preferring the requested theme with fallback to built-in."""
    if theme:
        try:
            return render_with_theme(resume, theme)
        except Exception as exc:  # noqa: BLE001 - any theme failure falls back to the built-in template
            if console:
                console.print(
                    f"[yellow]⚠ Theme '{theme}' failed ({exc}), using built-in template.[/yellow]"
                )
    return render_builtin(resume)
