"""Filtering logic: section selection and date-based cutoff."""

from __future__ import annotations

import copy
from datetime import date
from typing import Any

from .models import ALL_SECTIONS, DATE_FIELD_MAP


def _parse_iso_date(value: str | None) -> date | None:
    """Parse an ISO 8601 partial date string (YYYY, YYYY-MM, YYYY-MM-DD) to a date."""
    if not value:
        return None
    parts = value.strip().split("-")
    try:
        year = int(parts[0])
        month = int(parts[1]) if len(parts) > 1 else 1
        day = int(parts[2]) if len(parts) > 2 else 1
        return date(year, month, day)
    except (ValueError, IndexError):
        return None


def apply_section_filter(resume: dict[str, Any], sections: list[str]) -> dict[str, Any]:
    """Return a copy of resume containing only the requested sections.

    ``basics`` and ``meta`` are always preserved unless explicitly excluded.
    """
    result: dict[str, Any] = {}

    # Always carry schema ref and meta through if present
    if "$schema" in resume:
        result["$schema"] = resume["$schema"]
    if "meta" in resume:
        result["meta"] = resume["meta"]

    for key, value in resume.items():
        if key in ("$schema", "meta"):
            continue
        if key in sections or key not in ALL_SECTIONS:
            # Include unknown keys (custom extensions) unconditionally
            result[key] = copy.deepcopy(value)

    return result


def apply_date_cutoff(resume: dict[str, Any], cut_date: date) -> dict[str, Any]:
    """Return a copy of resume with entries older than cut_date removed.

    An entry is kept when:
    - It has no date field, OR
    - Its primary date field is on or after cut_date.

    For sections that track employment/projects (work, volunteer, education,
    projects) a position that *started* before the cut date but is *still
    ongoing* (no endDate) is kept, because the person is still in that role.
    """
    result = copy.deepcopy(resume)

    for section, date_field in DATE_FIELD_MAP.items():
        if section not in result or not isinstance(result[section], list):
            continue

        keep_ongoing = date_field == "startDate"
        filtered = []

        for entry in result[section]:
            entry_date = _parse_iso_date(entry.get(date_field))

            if entry_date is None:
                # No date info → keep unconditionally
                filtered.append(entry)
                continue

            if entry_date >= cut_date:
                filtered.append(entry)
            elif keep_ongoing and entry.get("endDate") is None:
                # Ongoing role that started before cut_date — keep it
                filtered.append(entry)

        result[section] = filtered

    return result


def available_summaries(resume: dict[str, Any]) -> dict[str, str]:
    """Return the ``meta.summaries`` variant map, or an empty dict if absent."""
    meta = resume.get("meta") or {}
    summaries = meta.get("summaries") or {}
    return summaries if isinstance(summaries, dict) else {}


def apply_summary_variant(resume: dict[str, Any], key: str) -> dict[str, Any]:
    """Return a copy of resume with ``basics.summary`` replaced by a named variant.

    Variants live in ``meta.summaries``.  Raises ``KeyError`` if *key* is not
    defined, with the available keys attached as the exception argument.
    """
    result = copy.deepcopy(resume)
    summaries = available_summaries(result)

    if key not in summaries:
        raise KeyError(key, sorted(summaries))

    result.setdefault("basics", {})["summary"] = summaries[key]
    return result


def strip_summary_map(resume: dict[str, Any]) -> dict[str, Any]:
    """Remove ``meta.summaries`` so the variant map never leaks into output."""
    result = copy.deepcopy(resume)
    meta = result.get("meta")
    if isinstance(meta, dict):
        meta.pop("summaries", None)
    return result


def filter_resume(
    resume: dict[str, Any],
    sections: list[str] | None,
    cut_date: date | None,
    summary: str | None = None,
) -> dict[str, Any]:
    """Apply summary variant, section filter and date cutoff in sequence."""
    result = copy.deepcopy(resume)

    if summary is not None:
        result = apply_summary_variant(result, summary)

    if sections is not None:
        result = apply_section_filter(result, sections)

    if cut_date is not None:
        result = apply_date_cutoff(result, cut_date)

    # The variant map is authoring metadata, not resume content.
    return strip_summary_map(result)
