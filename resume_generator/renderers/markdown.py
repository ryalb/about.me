"""Markdown renderer for JSON Resume data."""

from __future__ import annotations

from typing import Any

from ..contact import profile_display
from ..i18n import (
    format_date_range,
    language_of,
    load_locale,
    present_label,
    section_labels,
    t,
    work_cutoff_notice,
)


def _date_range(
    start: str | None, end: str | None, present: str, language: str = "en-US"
) -> str:
    return format_date_range(start, end, present, language)


def _section_header(title: str) -> str:
    return f"\n## {title}\n\n"


def render_markdown(resume: dict[str, Any], locale: str | None = None) -> str:
    """Render a JSON Resume dict to a Markdown string."""
    lines: list[str] = []
    locale_data = load_locale(resume, locale)
    present = present_label(locale_data)
    labels = section_labels(locale_data)
    language = language_of(resume, locale)

    # ── Basics ────────────────────────────────────────────────────────────
    basics = resume.get("basics") or {}
    name = basics.get("name") or t(locale_data, "untitled", default="Resume")
    lines.append(f"# {name}\n")

    if label := basics.get("label"):
        lines.append(f"**{label}**\n")

    contact: list[str] = []
    if email := basics.get("email"):
        contact.append(f"✉ [{email}](mailto:{email})")
    if phone := basics.get("phone"):
        contact.append(f"📞 {phone}")
    if url := basics.get("url"):
        contact.append(f"🌐 [{url}]({url})")
    if loc := basics.get("location"):
        parts = [loc.get("city"), loc.get("region"), loc.get("countryCode")]
        loc_str = ", ".join(p for p in parts if p)
        if loc_str:
            contact.append(f"📍 {loc_str}")
    for profile in basics.get("profiles") or []:
        shown = profile_display(profile)
        if not shown:
            continue
        purl = profile.get("url", "")
        text = f"[{shown}]({purl})" if purl else shown
        contact.append(f"🔗 {text}")

    if contact:
        lines.append(" | ".join(contact) + "\n")

    if summary := basics.get("summary"):
        lines.append(f"\n{summary}\n")

    for key, value in resume.items():
        if key in ("basics", "meta", "$schema"):
            continue
        if not isinstance(value, list) or not value:
            continue

        if key == "skills" and labels.get("skills"):
            lines.append(_section_header(labels["skills"]))
            for skill in value:
                sname = skill.get("name") or ""
                level = skill.get("level") or ""
                kws = skill.get("keywords") or []
                skill_line = f"**{sname}**"
                if level:
                    skill_line += f" ({level})"
                if kws:
                    skill_line += ": " + ", ".join(f"`{k}`" for k in kws)
                lines.append(f"{skill_line}\n\n")

        elif key == "work" and labels.get("work"):
            lines.append(_section_header(labels["work"]))
            for job in value:
                title = job.get("position") or ""
                company = job.get("name") or ""
                location = job.get("location") or ""
                url = job.get("url") or ""
                dr = _date_range(
                    job.get("startDate"), job.get("endDate"), present, language
                )
                company_str = f"[{company}]({url})" if url else company
                header = f"### {title}"
                if company_str:
                    header += f" — {company_str}"
                lines.append(f"{header}\n")
                meta_parts = []
                if location:
                    meta_parts.append(f"📍 {location}")
                if dr:
                    meta_parts.append(f"🗓 {dr}")
                if meta_parts:
                    lines.append("_" + " · ".join(meta_parts) + "_\n")
                if summary := job.get("summary"):
                    lines.append(f"\n{summary}\n")
                for h in job.get("highlights") or []:
                    lines.append(f"- {h}\n")
                lines.append("\n")
            if notice := work_cutoff_notice(resume, locale_data):
                lines.append(f"> _{notice}_\n\n")

        elif key == "projects" and labels.get("projects"):
            lines.append(_section_header(labels["projects"]))
            for proj in value:
                pname = proj.get("name") or ""
                purl = proj.get("url") or ""
                dr = _date_range(
                    proj.get("startDate"), proj.get("endDate"), present, language
                )
                title_str = f"[{pname}]({purl})" if purl else pname
                lines.append(f"### {title_str}\n")
                meta_parts = []
                if proj.get("type"):
                    meta_parts.append(proj["type"])
                if dr:
                    meta_parts.append(f"🗓 {dr}")
                if meta_parts:
                    lines.append("_" + " · ".join(meta_parts) + "_\n")
                if desc := proj.get("description"):
                    lines.append(f"\n{desc}\n")
                kws = proj.get("keywords") or []
                if kws:
                    lines.append("`" + "` `".join(kws) + "`\n")
                for h in proj.get("highlights") or []:
                    lines.append(f"- {h}\n")
                lines.append("\n")

        elif key == "volunteer" and labels.get("volunteer"):
            lines.append(_section_header(labels["volunteer"]))
            for v in value:
                pos = v.get("position") or ""
                org = v.get("organization") or ""
                dr = _date_range(
                    v.get("startDate"), v.get("endDate"), present, language
                )
                header = f"### {pos}"
                if org:
                    header += f" — {org}"
                lines.append(f"{header}\n")
                if dr:
                    lines.append(f"_🗓 {dr}_\n")
                if s := v.get("summary"):
                    lines.append(f"\n{s}\n")
                for h in v.get("highlights") or []:
                    lines.append(f"- {h}\n")
                lines.append("\n")

        elif key == "education" and labels.get("education"):
            lines.append(_section_header(labels["education"]))
            for edu in value:
                in_label = t(locale_data, "education", "in", default="in")
                degree = " ".join(
                    filter(
                        None,
                        [
                            edu.get("studyType"),
                            edu.get("area") and f"{in_label} {edu['area']}",
                        ],
                    )
                )
                institution = edu.get("institution") or ""
                dr = _date_range(
                    edu.get("startDate"), edu.get("endDate"), present, language
                )
                header = f"### {degree}" if degree else f"### {labels['education']}"
                if institution:
                    header += f" — {institution}"
                lines.append(f"{header}\n")
                if dr:
                    lines.append(f"_🗓 {dr}_\n")
                score_label = t(locale_data, "education", "score", default="Score:")
                if score := edu.get("score"):
                    lines.append(f"{score_label} {score}\n")
                workload_label = t(
                    locale_data, "education", "workload", default="Workload:"
                )
                if workload := edu.get("workload"):
                    lines.append(f"{workload_label} {workload}\n")
                for c in edu.get("courses") or []:
                    lines.append(f"- {c}\n")
                lines.append("\n")

        elif key == "certificates" and labels.get("certificates"):
            lines.append(_section_header(labels["certificates"]))
            for c in value:
                cname = c.get("name") or ""
                curl = c.get("url") or ""
                issuer = c.get("issuer") or ""
                cdate = c.get("date") or ""
                name_str = f"[{cname}]({curl})" if curl else cname
                lines.append(f"- **{name_str}**")
                parts = []
                if issuer:
                    parts.append(issuer)
                if cdate:
                    parts.append(cdate)
                if parts:
                    lines.append(f" · {' · '.join(parts)}")
                lines.append("\n")
            lines.append("\n")

        elif key == "publications" and labels.get("publications"):
            lines.append(_section_header(labels["publications"]))
            for pub in value:
                pname = pub.get("name") or ""
                purl = pub.get("url") or ""
                publisher = pub.get("publisher") or ""
                pdate = pub.get("releaseDate") or ""
                name_str = f"[{pname}]({purl})" if purl else pname
                lines.append(f"### {name_str}\n")
                meta = []
                if publisher:
                    meta.append(publisher)
                if pdate:
                    meta.append(pdate)
                if meta:
                    lines.append("_" + " · ".join(meta) + "_\n")
                if s := pub.get("summary"):
                    lines.append(f"\n{s}\n")
                lines.append("\n")

        elif key == "awards" and labels.get("awards"):
            lines.append(_section_header(labels["awards"]))
            for a in value:
                title = a.get("title") or ""
                aurl = a.get("url") or ""
                awarder = a.get("awarder") or ""
                adate = a.get("date") or ""
                title_str = f"[{title}]({aurl})" if aurl else title
                lines.append(f"### {title_str}\n")
                meta = []
                if awarder:
                    meta.append(awarder)
                if adate:
                    meta.append(adate)
                if meta:
                    lines.append("_" + " · ".join(meta) + "_\n")
                if s := a.get("summary"):
                    lines.append(f"\n{s}\n")
                lines.append("\n")

        elif key == "languages" and labels.get("languages"):
            lines.append(_section_header(labels["languages"]))
            for lang in value:
                lname = lang.get("language") or ""
                fluency = lang.get("fluency") or ""
                part = f"**{lname}**"
                if fluency:
                    part += f": {fluency}"
                lines.append(f"- {part}\n")
            lines.append("\n")

        elif key == "interests" and labels.get("interests"):
            lines.append(_section_header(labels["interests"]))
            for interest in value:
                iname = interest.get("name") or ""
                kws = interest.get("keywords") or []
                lines.append(f"- **{iname}**")
                if kws:
                    lines.append(f": {', '.join(kws)}")
                lines.append("\n")
            lines.append("\n")

        elif key == "references" and labels.get("references"):
            lines.append(_section_header(labels["references"]))
            for ref in value:
                rname = ref.get("name") or ""
                rtext = ref.get("reference") or ""
                lines.append(f"**{rname}**\n\n> {rtext}\n\n")

    return "".join(lines)
