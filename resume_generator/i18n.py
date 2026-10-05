"""Locale-dependent labels for generated output.

The language is resolved in this order:
1. ``--locale`` CLI flag
2. ``meta.language`` in the resume file (a BCP 47 tag, e.g. ``en-US`` or ``pt-BR``)
3. Default ``en-US``

Strings are loaded from ``resume_generator/locales/<tag>.json`` over English.  Only labels
the renderers emit themselves live here — resume *content* is translated by
maintaining one resume file per language.

The ``base`` theme resolves the same label in JavaScript (see
``custom/themes/base/src/Resume.jsx``); keep the two tables in step.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_DEFAULT_LANGUAGE = "en-US"
_FALLBACK_LANGUAGE = "en"
_LOCALES_DIR = Path(__file__).parent / "locales"

# Cache loaded locale tables.
_locale_cache: dict[str, dict[str, Any]] = {}


def _read_table(name: str) -> dict[str, Any] | None:
    path = _LOCALES_DIR / f"{name}.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively overlay *override* on *base* without mutating either."""
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _load_locale(tag: str) -> dict[str, Any]:
    """Load a locale table, overlaid on English so no key is ever missing.

    Lookup order: full tag (``pt-BR``) → bare language (``pt``).  A key absent
    from the chosen table falls back to the English string rather than to a
    hard-coded default at the call site.
    """
    if tag in _locale_cache:
        return _locale_cache[tag]

    english = _read_table(_FALLBACK_LANGUAGE) or {}
    table = english
    for candidate in dict.fromkeys((tag, tag.split("-")[0].lower())):
        if candidate == _FALLBACK_LANGUAGE:
            break
        if (found := _read_table(candidate)) is not None:
            table = _merge(english, found)
            break

    _locale_cache[tag] = table
    return table


def language_of(resume: dict[str, Any], cli_locale: str | None = None) -> str:
    """Return the effective language tag.

    Priority: CLI ``--locale`` flag > ``meta.language`` in the resume > default.
    """
    if cli_locale and cli_locale.strip():
        return cli_locale.strip()
    meta = resume.get("meta")
    if isinstance(meta, dict):
        language = meta.get("language")
        if isinstance(language, str) and language.strip():
            return language.strip()
    return _DEFAULT_LANGUAGE


def t(locale_data: dict[str, Any], *path: str, default: str = "") -> str:
    """Look up a translated string by dotted path, falling back to *default*."""
    node: Any = locale_data
    for key in path:
        if not isinstance(node, dict):
            return default
        node = node.get(key)
    return node if isinstance(node, str) else default


_PT_MONTHS = [
    "jan",
    "fev",
    "mar",
    "abr",
    "mai",
    "jun",
    "jul",
    "ago",
    "set",
    "out",
    "nov",
    "dez",
]
_EN_MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


def _months_for(language: str) -> list[str]:
    tag = (language or "en-US").split("-")[0].lower()
    if tag == "pt":
        return _PT_MONTHS
    return _EN_MONTHS


def format_date(date_str: str | None, language: str = "en-US") -> str:
    """Format a date string as MMM/YYYY with the first letter capitalized.

    Accepts ``YYYY``, ``YYYY-MM`` or ``YYYY-MM-DD``.  Year-only values are
    returned unchanged so that publications and awards that store only a year
    continue to render as just that year.
    """
    if not date_str:
        return ""
    if len(date_str) == 4 and date_str.isdigit():
        return date_str
    parts = date_str.split("-")
    year = parts[0]
    if len(parts) < 2:
        return date_str
    try:
        month = int(parts[1])
    except ValueError:
        return date_str
    if 1 <= month <= 12:
        months = _months_for(language)
        return f"{months[month - 1]}/{year}"
    return date_str


def format_date_range(
    start: str | None, end: str | None, present: str, language: str = "en-US"
) -> str:
    """Format a date range as ``MMM/YYYY - MMM/YYYY`` or ``MMM/YYYY - <present>``."""
    start_str = format_date(start, language)
    end_str = format_date(end, language) if end else (start_str and present or "")
    if start_str and end_str:
        return f"{start_str} - {end_str}"
    return start_str or end_str or ""


def present_label(locale_data: dict[str, Any]) -> str:
    """Return the label marking an entry with no end date as still ongoing."""
    return t(locale_data, "present", default="Present")


def section_labels(locale_data: dict[str, Any]) -> dict[str, str]:
    """Return the section-heading table for the locale."""
    sections = locale_data.get("section")
    return dict(sections) if isinstance(sections, dict) else {}


def work_cutoff_notice(
    resume: dict[str, Any], locale_data: dict[str, Any]
) -> str | None:
    """Return the disclosure line for a date-trimmed work history, or None."""
    meta = resume.get("meta")
    filtered = meta.get("filtered") if isinstance(meta, dict) else None
    if not isinstance(filtered, dict):
        return None
    hidden = filtered.get("hidden")
    count = hidden.get("work", 0) if isinstance(hidden, dict) else 0
    if not count:
        return None

    template = t(locale_data, "cutoff_notice", "one" if count == 1 else "many")
    if not template:
        return None
    return template.format(count=count, date=filtered.get("cutDate") or "")


def load_locale(
    resume: dict[str, Any], cli_locale: str | None = None
) -> dict[str, Any]:
    """Resolve the effective locale and return its string table."""
    return _load_locale(language_of(resume, cli_locale))
