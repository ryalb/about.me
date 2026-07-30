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

# Section headings the renderers emit themselves.  The English entries are the
# wording md/txt/docx have always used — the ``base`` theme keeps its own,
# shorter set ("Experience", "Certificates") in Resume.jsx.
#
# Only the languages this repo maintains a resume file for are translated;
# anything else falls back to English, which is still better than a missing
# heading.  Add a language here and in Resume.jsx's SECTION_LABELS together.
_SECTION_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "summary": "Summary",
        "work": "Work Experience",
        "education": "Education",
        "skills": "Skills",
        "projects": "Projects",
        "volunteer": "Volunteer",
        "awards": "Awards",
        "certificates": "Certifications",
        "publications": "Publications",
        "languages": "Languages",
        "interests": "Interests",
        "references": "References",
    },
    "pt": {
        "summary": "Resumo",
        "work": "Experiência Profissional",
        "education": "Formação Acadêmica",
        "skills": "Competências",
        "projects": "Projetos",
        "volunteer": "Trabalho Voluntário",
        "awards": "Prêmios",
        "certificates": "Certificações",
        "publications": "Publicações",
        "languages": "Idiomas",
        "interests": "Interesses",
        "references": "Referências",
    },
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


def section_labels(resume: dict[str, Any]) -> dict[str, str]:
    """Return the section-heading table for the resume's language.

    Missing languages fall back to English rather than to the raw section key,
    so a heading is never emitted as ``certificates``.
    """
    language = language_of(resume)
    english = _SECTION_LABELS["en"]
    table = _SECTION_LABELS.get(language) or _SECTION_LABELS.get(
        language.split("-")[0].lower()
    )
    return {**english, **(table or {})}


# Disclosure for a date-trimmed work history.  Without it a reader cannot tell
# a filtered résumé from a short career, which misrepresents the candidate in
# the opposite direction from the usual one.  (singular, plural) per language.
#
# Keep in step with CUTOFF_NOTICES in custom/themes/base/src/Resume.jsx.
_WORK_CUTOFF_NOTICES = {
    "en": (
        (
            "Filtered view — 1 earlier role starting before {date} is not shown. "
            "Full history available on request."
        ),
        (
            "Filtered view — {count} earlier roles starting before {date} are not "
            "shown. Full history available on request."
        ),
    ),
    "pt": (
        (
            "Visão filtrada — 1 cargo anterior, iniciado antes de {date}, não está "
            "sendo exibido. Histórico completo disponível sob solicitação."
        ),
        (
            "Visão filtrada — {count} cargos anteriores, iniciados antes de {date}, "
            "não estão sendo exibidos. Histórico completo disponível sob solicitação."
        ),
    ),
}


def work_cutoff_notice(resume: dict[str, Any]) -> str | None:
    """Return the disclosure line for a date-trimmed work history, or None.

    Reads ``meta.filtered`` as written by :func:`filter.apply_date_cutoff`.
    Returns None when no cutoff was applied or when it removed no work entry,
    so callers can emit unconditionally.
    """
    meta = resume.get("meta")
    if not isinstance(meta, dict):
        return None
    filtered = meta.get("filtered")
    if not isinstance(filtered, dict):
        return None

    hidden = filtered.get("hidden")
    count = hidden.get("work", 0) if isinstance(hidden, dict) else 0
    if not count:
        return None

    language = language_of(resume)
    table = (
        _WORK_CUTOFF_NOTICES.get(language)
        or _WORK_CUTOFF_NOTICES.get(language.split("-")[0].lower())
        or _WORK_CUTOFF_NOTICES["en"]
    )
    template = table[0] if count == 1 else table[1]
    return template.format(count=count, date=filtered.get("cutDate") or "")
