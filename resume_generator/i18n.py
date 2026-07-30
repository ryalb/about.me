"""Locale-dependent labels for generated output.

The language is read from ``meta.language`` in the resume file (a BCP 47 tag,
e.g. ``en-US`` or ``pt-BR``).  Only labels the renderers emit themselves live
here — resume *content* is translated by maintaining one file per language.

The ``base`` theme resolves the same label in JavaScript (see
``custom/themes/base/src/Resume.jsx``); keep the two tables in step.
"""

from __future__ import annotations

from typing import Any

DEFAULT_LANGUAGE = "en-US"

# Keyed by full BCP 47 tag first, then by the bare language subtag.
_PRESENT_LABELS = {
    "en": "Present",
    "pt": "Presente",
    "es": "Presente",
    "fr": "Présent",
    "it": "Presente",
    "de": "Heute",
}


def language_of(resume: dict[str, Any]) -> str:
    """Return the resume's ``meta.language`` tag, or the default."""
    meta = resume.get("meta")
    if isinstance(meta, dict):
        language = meta.get("language")
        if isinstance(language, str) and language.strip():
            return language.strip()
    return DEFAULT_LANGUAGE


def present_label(resume: dict[str, Any]) -> str:
    """Return the label marking an entry with no end date as still ongoing.

    An omitted ``endDate`` is the JSON Resume convention for ongoing work, so
    every date-range section renders this label in place of the missing date.
    """
    language = language_of(resume)
    return (
        _PRESENT_LABELS.get(language)
        or _PRESENT_LABELS.get(language.split("-")[0].lower())
        or _PRESENT_LABELS["en"]
    )
