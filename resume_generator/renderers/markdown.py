"""Markdown renderer for JSON Resume data."""

from __future__ import annotations

from typing import Any

from ..contact import profile_display
from ..i18n import present_label, section_labels, work_cutoff_notice


def _date_range(start: str | None, end: str | None, present: str) -> str:
    if not start and not end:
        return ""
    if start and end:
        return f"{start} – {end}"
    if start:
        return f"{start} – {present}"
    return end or ""


def _section_header(title: str) -> str:
    return f"\n## {title}\n\n"


def render_markdown(resume: dict[str, Any]) -> str:
    """Render a JSON Resume dict to a Markdown string."""
    lines: list[str] = []
    present = present_label(resume)
    labels = section_labels(resume)

    # ── Basics ────────────────────────────────────────────────────────────
    basics = resume.get("basics") or {}
    name = basics.get("name") or "Resume"
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

    # ── Skills ────────────────────────────────────────────────────────────
    if skills := resume.get("skills"):
        lines.append(_section_header(labels["skills"]))
        for skill in skills:
            sname = skill.get("name") or ""
            level = skill.get("level") or ""
            kws = skill.get("keywords") or []
            skill_line = f"**{sname}**"
            if level:
                skill_line += f" ({level})"
            if kws:
                skill_line += ": " + ", ".join(f"`{k}`" for k in kws)
            lines.append(f"{skill_line}\n\n")

    # ── Work ──────────────────────────────────────────────────────────────
    if work := resume.get("work"):
        lines.append(_section_header(labels["work"]))
        for job in work:
            title = job.get("position") or ""
            company = job.get("name") or ""
            location = job.get("location") or ""
            url = job.get("url") or ""
            dr = _date_range(job.get("startDate"), job.get("endDate"), present)
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
        if notice := work_cutoff_notice(resume):
            lines.append(f"> _{notice}_\n\n")

    # ── Projects ──────────────────────────────────────────────────────────
    if projects := resume.get("projects"):
        lines.append(_section_header(labels["projects"]))
        for proj in projects:
            pname = proj.get("name") or ""
            purl = proj.get("url") or ""
            dr = _date_range(proj.get("startDate"), proj.get("endDate"), present)
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

    # ── Volunteer ─────────────────────────────────────────────────────────
    if volunteer := resume.get("volunteer"):
        lines.append(_section_header(labels["volunteer"]))
        for v in volunteer:
            pos = v.get("position") or ""
            org = v.get("organization") or ""
            dr = _date_range(v.get("startDate"), v.get("endDate"), present)
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

    # ── Education ─────────────────────────────────────────────────────────
    if education := resume.get("education"):
        lines.append(_section_header(labels["education"]))
        for edu in education:
            degree = " ".join(
                filter(
                    None,
                    [
                        edu.get("studyType"),
                        "in" if edu.get("area") else "",
                        edu.get("area"),
                    ],
                )
            )
            institution = edu.get("institution") or ""
            dr = _date_range(edu.get("startDate"), edu.get("endDate"), present)
            header = f"### {degree}" if degree else f"### {labels['education']}"
            if institution:
                header += f" — {institution}"
            lines.append(f"{header}\n")
            if dr:
                lines.append(f"_🗓 {dr}_\n")
            if score := edu.get("score"):
                lines.append(f"Score: {score}\n")
            for c in edu.get("courses") or []:
                lines.append(f"- {c}\n")
            lines.append("\n")

    # ── Certificates ──────────────────────────────────────────────────────
    if certs := resume.get("certificates"):
        lines.append(_section_header(labels["certificates"]))
        for c in certs:
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

    # ── Publications ──────────────────────────────────────────────────────
    if pubs := resume.get("publications"):
        lines.append(_section_header(labels["publications"]))
        for pub in pubs:
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

    # ── Awards ────────────────────────────────────────────────────────────
    if awards := resume.get("awards"):
        lines.append(_section_header(labels["awards"]))
        for a in awards:
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

    # ── Languages ─────────────────────────────────────────────────────────
    if langs := resume.get("languages"):
        lines.append(_section_header(labels["languages"]))
        for lang in langs:
            lname = lang.get("language") or ""
            fluency = lang.get("fluency") or ""
            part = f"**{lname}**"
            if fluency:
                part += f": {fluency}"
            lines.append(f"- {part}\n")
        lines.append("\n")

    # ── Interests ─────────────────────────────────────────────────────────
    if interests := resume.get("interests"):
        lines.append(_section_header(labels["interests"]))
        for interest in interests:
            iname = interest.get("name") or ""
            kws = interest.get("keywords") or []
            lines.append(f"- **{iname}**")
            if kws:
                lines.append(f": {', '.join(kws)}")
            lines.append("\n")
        lines.append("\n")

    # ── References ────────────────────────────────────────────────────────
    if refs := resume.get("references"):
        lines.append(_section_header(labels["references"]))
        for ref in refs:
            rname = ref.get("name") or ""
            rtext = ref.get("reference") or ""
            lines.append(f"**{rname}**\n\n> {rtext}\n\n")

    return "".join(lines)
