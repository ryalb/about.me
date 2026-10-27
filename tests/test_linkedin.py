"""LinkedIn sheet: paste-ready fields and limit reporting."""

from resume_generator.renderers.linkedin import (
    LIMITS,
    linkedin_overflows,
    render_linkedin,
)


def _resume(**work):
    job = {"position": "Engineer", "name": "ACME", "startDate": "2020-01", **work}
    return {"basics": {"name": "Ana", "label": "Engineer"}, "work": [job]}


def test_highlights_become_bullet_lines():
    sheet = render_linkedin(_resume(summary="Builds things.", highlights=["Shipped"]))
    assert "Builds things.\n\n• Shipped" in sheet


def test_open_role_is_marked_current():
    assert "I am currently working in this role" in render_linkedin(_resume())


def test_labels_follow_locale():
    sheet = render_linkedin(_resume(), locale="pt-BR")
    assert "Cargo: Engineer" in sheet and "EXPERIÊNCIA" in sheet


def test_overlong_description_is_reported():
    resume = _resume(summary="x" * (LIMITS["description"] + 1))
    assert "OVER LIMIT" in render_linkedin(resume)
    assert any("2001/2000" in p for p in linkedin_overflows(resume))


def test_skills_are_flattened_and_deduplicated():
    resume = {"skills": [{"keywords": ["Python", "SQL"]}, {"keywords": ["python"]}]}
    assert "Total skills: 2/100" in render_linkedin(resume)


def test_linkedin_is_always_generated():
    from resume_generator.main import _parse_formats

    assert _parse_formats("html,pdf") == ["html", "pdf", "linkedin"]
    assert _parse_formats("linkedin,md") == ["linkedin", "md"]
