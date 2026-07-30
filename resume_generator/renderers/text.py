"""Plain-text renderer for JSON Resume data."""

from __future__ import annotations

import textwrap
from typing import Any

from ..contact import profile_display
from ..i18n import present_label, section_labels, work_cutoff_notice

_WIDTH = 80
_SEP = "─" * _WIDTH


def _date_range(start: str | None, end: str | None, present: str) -> str:
    if not start and not end:
        return ""
    if start and end:
        return f"{start} – {end}"
    if start:
        return f"{start} – {present}"
    return end or ""


def _wrap(text: str, indent: int = 0) -> str:
    prefix = " " * indent
    return textwrap.fill(
        text, width=_WIDTH, initial_indent=prefix, subsequent_indent=prefix
    )


def _section(title: str) -> str:
    return f"\n{title.upper()}\n{_SEP}\n"


def render_text(resume: dict[str, Any]) -> str:
    lines: list[str] = []
    present = present_label(resume)
    labels = section_labels(resume)

    # ── Basics ────────────────────────────────────────────────────────────
    basics = resume.get("basics") or {}
    name = basics.get("name") or "Resume"
    lines.append(name.upper().center(_WIDTH))
    if label := basics.get("label"):
        lines.append(label.center(_WIDTH))
    lines.append(_SEP)

    contact: list[str] = []
    if email := basics.get("email"):
        contact.append(email)
    if phone := basics.get("phone"):
        contact.append(phone)
    if url := basics.get("url"):
        contact.append(url)
    if loc := basics.get("location"):
        parts = [loc.get("city"), loc.get("region"), loc.get("countryCode")]
        loc_str = ", ".join(p for p in parts if p)
        if loc_str:
            contact.append(loc_str)
    for profile in basics.get("profiles") or []:
        if shown := profile_display(profile):
            contact.append(shown)
    if contact:
        lines.append("  ".join(contact).center(_WIDTH))
    lines.append("")

    if summary := basics.get("summary"):
        lines.append(_wrap(summary))
        lines.append("")

    # ── Work ──────────────────────────────────────────────────────────────
    if work := resume.get("work"):
        lines.append(_section(labels["work"]))
        for job in work:
            pos = job.get("position") or ""
            company = job.get("name") or ""
            loc = job.get("location") or ""
            dr = _date_range(job.get("startDate"), job.get("endDate"), present)
            left = f"{pos}" + (f" @ {company}" if company else "")
            right = dr
            pad = _WIDTH - len(left) - len(right)
            lines.append(left + " " * max(1, pad) + right)
            if loc:
                lines.append(f"  {loc}")
            if s := job.get("summary"):
                lines.append(_wrap(s, indent=2))
            for h in job.get("highlights") or []:
                lines.append(_wrap(f"• {h}", indent=4))
            lines.append("")
        if notice := work_cutoff_notice(resume):
            lines.append(_wrap(f"[ {notice} ]", indent=2))
            lines.append("")

    # ── Education ─────────────────────────────────────────────────────────
    if education := resume.get("education"):
        lines.append(_section(labels["education"]))
        for edu in education:
            degree_parts = [edu.get("studyType"), edu.get("area")]
            degree = ", ".join(p for p in degree_parts if p)
            institution = edu.get("institution") or ""
            dr = _date_range(edu.get("startDate"), edu.get("endDate"), present)
            left = degree + (f" — {institution}" if institution else "")
            pad = _WIDTH - len(left) - len(dr)
            lines.append(left + " " * max(1, pad) + dr)
            if score := edu.get("score"):
                lines.append(f"  GPA/Score: {score}")
            for c in edu.get("courses") or []:
                lines.append(f"  • {c}")
            lines.append("")

    # ── Skills ────────────────────────────────────────────────────────────
    if skills := resume.get("skills"):
        lines.append(_section(labels["skills"]))
        for skill in skills:
            sname = skill.get("name") or ""
            level = skill.get("level") or ""
            kws = skill.get("keywords") or []
            header = sname + (f" ({level})" if level else "")
            kw_str = ", ".join(kws)
            if kw_str:
                lines.append(_wrap(f"{header}: {kw_str}", indent=0))
            else:
                lines.append(header)
        lines.append("")

    # ── Projects ──────────────────────────────────────────────────────────
    if projects := resume.get("projects"):
        lines.append(_section(labels["projects"]))
        for proj in projects:
            pname = proj.get("name") or ""
            dr = _date_range(proj.get("startDate"), proj.get("endDate"), present)
            ptype = proj.get("type") or ""
            right = " | ".join(filter(None, [ptype, dr]))
            pad = _WIDTH - len(pname) - len(right)
            lines.append(pname + " " * max(1, pad) + right)
            if desc := proj.get("description"):
                lines.append(_wrap(desc, indent=2))
            kws = proj.get("keywords") or []
            if kws:
                lines.append(_wrap(f"  [{', '.join(kws)}]", indent=2))
            for h in proj.get("highlights") or []:
                lines.append(_wrap(f"• {h}", indent=4))
            lines.append("")

    # ── Volunteer ─────────────────────────────────────────────────────────
    if volunteer := resume.get("volunteer"):
        lines.append(_section(labels["volunteer"]))
        for v in volunteer:
            pos = v.get("position") or ""
            org = v.get("organization") or ""
            dr = _date_range(v.get("startDate"), v.get("endDate"), present)
            left = pos + (f" @ {org}" if org else "")
            pad = _WIDTH - len(left) - len(dr)
            lines.append(left + " " * max(1, pad) + dr)
            if s := v.get("summary"):
                lines.append(_wrap(s, indent=2))
            for h in v.get("highlights") or []:
                lines.append(_wrap(f"• {h}", indent=4))
            lines.append("")

    # ── Awards ────────────────────────────────────────────────────────────
    if awards := resume.get("awards"):
        lines.append(_section(labels["awards"]))
        for a in awards:
            title = a.get("title") or ""
            awarder = a.get("awarder") or ""
            adate = a.get("date") or ""
            right = " | ".join(filter(None, [awarder, adate]))
            pad = _WIDTH - len(title) - len(right)
            lines.append(title + " " * max(1, pad) + right)
            if s := a.get("summary"):
                lines.append(_wrap(s, indent=2))
            if aurl := a.get("url"):
                lines.append(f"  {aurl}")
            lines.append("")

    # ── Certificates ──────────────────────────────────────────────────────
    if certs := resume.get("certificates"):
        lines.append(_section(labels["certificates"]))
        for c in certs:
            cname = c.get("name") or ""
            issuer = c.get("issuer") or ""
            cdate = c.get("date") or ""
            right = " | ".join(filter(None, [issuer, cdate]))
            pad = _WIDTH - len(cname) - len(right)
            lines.append(cname + " " * max(1, pad) + right)
            if curl := c.get("url"):
                lines.append(f"  {curl}")
        lines.append("")

    # ── Publications ──────────────────────────────────────────────────────
    if pubs := resume.get("publications"):
        lines.append(_section(labels["publications"]))
        for pub in pubs:
            pname = pub.get("name") or ""
            publisher = pub.get("publisher") or ""
            pdate = pub.get("releaseDate") or ""
            right = " | ".join(filter(None, [publisher, pdate]))
            pad = _WIDTH - len(pname) - len(right)
            lines.append(pname + " " * max(1, pad) + right)
            if s := pub.get("summary"):
                lines.append(_wrap(s, indent=2))
            if purl := pub.get("url"):
                lines.append(f"  {purl}")
            lines.append("")

    # ── Languages ─────────────────────────────────────────────────────────
    if langs := resume.get("languages"):
        lines.append(_section(labels["languages"]))
        parts = []
        for lang in langs:
            lname = lang.get("language") or ""
            fluency = lang.get("fluency") or ""
            parts.append(lname + (f" ({fluency})" if fluency else ""))
        lines.append("  " + " | ".join(parts))
        lines.append("")

    # ── Interests ─────────────────────────────────────────────────────────
    if interests := resume.get("interests"):
        lines.append(_section(labels["interests"]))
        for interest in interests:
            iname = interest.get("name") or ""
            kws = interest.get("keywords") or []
            part = iname
            if kws:
                part += f": {', '.join(kws)}"
            lines.append(f"  • {part}")
        lines.append("")

    # ── References ────────────────────────────────────────────────────────
    if refs := resume.get("references"):
        lines.append(_section(labels["references"]))
        for ref in refs:
            rname = ref.get("name") or ""
            rtext = ref.get("reference") or ""
            lines.append(f"  {rname}")
            lines.append(_wrap(f'  "{rtext}"', indent=4))
            lines.append("")

    return "\n".join(lines)
