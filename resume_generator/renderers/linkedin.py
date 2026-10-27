"""LinkedIn copy-paste sheet for JSON Resume data.

LinkedIn offers no API for editing your own profile, so the profile is updated
by hand.  This renderer lays the resume out field by field, in the order the
LinkedIn edit forms ask for it, so each block can be pasted as-is.

LinkedIn fields are plain text: Markdown is shown literally and there are no
lists, so highlights become ``•`` lines.  Fields with a known character limit
carry a ``[used/limit]`` counter; :func:`linkedin_overflows` reports the ones
that would be truncated.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..i18n import format_date, language_of, load_locale, t

# Limits enforced by the LinkedIn profile editor.  Fields not listed here are
# either short by nature or have no documented limit.
LIMITS = {
    "headline": 220,
    "about": 2600,
    "title": 100,
    "company": 100,
    "description": 2000,
    "education_description": 1000,
    "skill": 80,
    "skills_total": 100,
}

_WIDTH = 80
_RULE = "═" * _WIDTH


@dataclass(frozen=True)
class _Field:
    label: str
    value: str
    limit: int | None = None
    multiline: bool = False

    @property
    def over(self) -> bool:
        return self.limit is not None and len(self.value) > self.limit


@dataclass(frozen=True)
class _Section:
    title: str
    entries: list[list[_Field]]


def _label(locale_data: dict[str, Any], key: str, default: str) -> str:
    return t(locale_data, "linkedin", key, default=default)


def _description(summary: str | None, bullets: list[str] | None) -> str:
    parts = [summary.strip()] if summary and summary.strip() else []
    if bullets:
        parts.append("\n".join(f"• {b}" for b in bullets))
    return "\n\n".join(parts)


def _location(loc: dict[str, Any] | None) -> str:
    if not loc:
        return ""
    parts = [loc.get("city"), loc.get("region"), loc.get("countryCode")]
    return ", ".join(p for p in parts if p)


def _skills(resume: dict[str, Any]) -> list[str]:
    """Flatten skill groups into unique keywords; LinkedIn has no categories."""
    seen: dict[str, str] = {}
    for group in resume.get("skills") or []:
        for kw in group.get("keywords") or [group.get("name") or ""]:
            if kw and kw.casefold() not in seen:
                seen[kw.casefold()] = kw
    return list(seen.values())


def _sections(resume: dict[str, Any], locale: str | None) -> list[_Section]:
    ld = load_locale(resume, locale)
    language = language_of(resume, locale)
    current = _label(ld, "current", "I am currently working in this role")

    def date(value: str | None) -> str:
        return format_date(value, language)

    sections: list[_Section] = []
    basics = resume.get("basics") or {}

    intro = [
        _Field(
            _label(ld, "headline", "Headline"),
            basics.get("label") or "",
            LIMITS["headline"],
        ),
        _Field(_label(ld, "location", "Location"), _location(basics.get("location"))),
    ]
    contact = [
        _Field(_label(ld, "website", "Website"), basics.get("url") or ""),
        _Field(_label(ld, "email", "Email"), basics.get("email") or ""),
        _Field(_label(ld, "phone", "Phone"), basics.get("phone") or ""),
    ]
    sections.append(_Section(_label(ld, "intro", "Intro"), [intro, contact]))

    if summary := basics.get("summary"):
        about = _Field(_label(ld, "about", "About"), summary, LIMITS["about"], True)
        sections.append(_Section(_label(ld, "about", "About"), [[about]]))

    if work := resume.get("work"):
        entries = [
            [
                _Field(
                    _label(ld, "title", "Title"),
                    job.get("position") or "",
                    LIMITS["title"],
                ),
                _Field(
                    _label(ld, "company", "Company name"),
                    job.get("name") or "",
                    LIMITS["company"],
                ),
                _Field(_label(ld, "location", "Location"), job.get("location") or ""),
                _Field(
                    _label(ld, "start_date", "Start date"), date(job.get("startDate"))
                ),
                _Field(
                    _label(ld, "end_date", "End date"),
                    date(job.get("endDate")) if job.get("endDate") else f"☑ {current}",
                ),
                _Field(
                    _label(ld, "description", "Description"),
                    _description(job.get("summary"), job.get("highlights")),
                    LIMITS["description"],
                    True,
                ),
            ]
            for job in work
        ]
        sections.append(_Section(_label(ld, "experience", "Experience"), entries))

    if education := resume.get("education"):
        entries = []
        for edu in education:
            courses = edu.get("courses") or []
            entries.append(
                [
                    _Field(
                        _label(ld, "school", "School"), edu.get("institution") or ""
                    ),
                    _Field(_label(ld, "degree", "Degree"), edu.get("studyType") or ""),
                    _Field(
                        _label(ld, "field_of_study", "Field of study"),
                        edu.get("area") or "",
                    ),
                    _Field(
                        _label(ld, "start_date", "Start date"),
                        date(edu.get("startDate")),
                    ),
                    _Field(
                        _label(ld, "end_date", "End date"), date(edu.get("endDate"))
                    ),
                    _Field(_label(ld, "grade", "Grade"), edu.get("score") or ""),
                    _Field(
                        _label(ld, "description", "Description"),
                        _description(edu.get("summary"), courses),
                        LIMITS["education_description"],
                        True,
                    ),
                ]
            )
        sections.append(_Section(_label(ld, "education", "Education"), entries))

    if certificates := resume.get("certificates"):
        entries = [
            [
                _Field(_label(ld, "name", "Name"), c.get("name") or ""),
                _Field(
                    _label(ld, "issuer", "Issuing organization"), c.get("issuer") or ""
                ),
                _Field(_label(ld, "issue_date", "Issue date"), date(c.get("date"))),
                _Field(
                    _label(ld, "credential_url", "Credential URL"), c.get("url") or ""
                ),
            ]
            for c in certificates
        ]
        sections.append(
            _Section(_label(ld, "certifications", "Licenses & certifications"), entries)
        )

    if publications := resume.get("publications"):
        entries = [
            [
                _Field(_label(ld, "pub_title", "Title"), p.get("name") or ""),
                _Field(
                    _label(ld, "publisher", "Publication/Publisher"),
                    p.get("publisher") or "",
                ),
                _Field(
                    _label(ld, "publication_date", "Publication date"),
                    date(p.get("releaseDate")),
                ),
                _Field(_label(ld, "url", "Publication URL"), p.get("url") or ""),
                _Field(
                    _label(ld, "description", "Description"),
                    p.get("summary") or "",
                    LIMITS["description"],
                    True,
                ),
            ]
            for p in publications
        ]
        sections.append(_Section(_label(ld, "publications", "Publications"), entries))

    if awards := resume.get("awards"):
        entries = [
            [
                _Field(_label(ld, "pub_title", "Title"), a.get("title") or ""),
                _Field(_label(ld, "awarder", "Issuer"), a.get("awarder") or ""),
                _Field(_label(ld, "issue_date", "Issue date"), date(a.get("date"))),
                _Field(
                    _label(ld, "description", "Description"),
                    _description(a.get("summary"), [a["url"]] if a.get("url") else []),
                    LIMITS["description"],
                    True,
                ),
            ]
            for a in awards
        ]
        sections.append(_Section(_label(ld, "awards", "Honors & awards"), entries))

    if languages := resume.get("languages"):
        entries = [
            [
                _Field(_label(ld, "language", "Language"), lang.get("language") or ""),
                _Field(
                    _label(ld, "proficiency", "Proficiency"), lang.get("fluency") or ""
                ),
            ]
            for lang in languages
        ]
        sections.append(_Section(_label(ld, "languages", "Languages"), entries))

    if skills := _skills(resume):
        fields = [_Field("", s, LIMITS["skill"]) for s in skills]
        total = _Field(
            _label(ld, "skills_total", "Total skills"),
            f"{len(skills)}/{LIMITS['skills_total']}",
        )
        sections.append(_Section(_label(ld, "skills", "Skills"), [fields, [total]]))

    return sections


def _counter(field: _Field) -> str:
    if field.limit is None:
        return ""
    flag = "  ⚠ OVER LIMIT" if field.over else ""
    return f"  [{len(field.value)}/{field.limit}]{flag}"


def render_linkedin(resume: dict[str, Any], locale: str | None = None) -> str:
    ld = load_locale(resume, locale)
    name = (resume.get("basics") or {}).get("name") or ""
    lines = [
        f"LINKEDIN — {name}".rstrip(" —"),
        _label(
            ld,
            "instructions",
            "Paste each block into the matching LinkedIn field. "
            "[used/limit] shows the character count.",
        ),
    ]

    for section in _sections(resume, locale):
        lines += ["", _RULE, section.title.upper(), _RULE]
        for i, entry in enumerate(section.entries):
            fields = [f for f in entry if f.value]
            if not fields:
                continue
            if i:
                lines.append("─" * _WIDTH)
            for field in fields:
                if not field.label:
                    lines.append(f"{field.value}{_counter(field)}")
                elif field.multiline:
                    lines += ["", f"{field.label}:{_counter(field)}", field.value, ""]
                else:
                    lines.append(f"{field.label}: {field.value}{_counter(field)}")

    return "\n".join(lines)


def linkedin_overflows(resume: dict[str, Any], locale: str | None = None) -> list[str]:
    """Describe every field longer than LinkedIn accepts."""
    problems = []
    for section in _sections(resume, locale):
        for entry in section.entries:
            for field in entry:
                if field.over:
                    head = field.value.splitlines()[0][:40]
                    problems.append(
                        f"{section.title} › {field.label or head}: "
                        f"{len(field.value)}/{field.limit} chars"
                    )
    if (count := len(_skills(resume))) > LIMITS["skills_total"]:
        problems.append(f"Skills: {count}/{LIMITS['skills_total']} entries")
    return problems
