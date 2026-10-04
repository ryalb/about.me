"""Locale tables stay complete and in step across Python and the base theme."""

import json
from pathlib import Path

from resume_generator.i18n import load_locale, section_labels, work_cutoff_notice

ROOT = Path(__file__).parent.parent
PY_LOCALES = ROOT / "resume_generator" / "locales"
THEME_LOCALES = ROOT / "custom" / "themes" / "base" / "locales"


def _keys(node, prefix=""):
    if not isinstance(node, dict):
        return {prefix}
    return {k for key, v in node.items() for k in _keys(v, f"{prefix}{key}.")}


def test_every_locale_has_every_english_key():
    for directory in (PY_LOCALES, THEME_LOCALES):
        english = _keys(json.loads((directory / "en.json").read_text()))
        for path in directory.glob("*.json"):
            assert english <= _keys(json.loads(path.read_text())), path


def test_portuguese_sections_are_not_english():
    labels = section_labels(load_locale({"meta": {"language": "pt-BR"}}))
    assert labels["education"] == "Formação Acadêmica"


def test_partial_locale_falls_back_per_key():
    labels = section_labels(load_locale({}, "xx-YY"))
    assert labels["work"] == "Work Experience"


def test_cutoff_notice_is_translated_and_pluralised():
    resume = {
        "meta": {
            "language": "pt-BR",
            "filtered": {"cutDate": "2015-01-01", "hidden": {"work": 2}},
        }
    }
    notice = work_cutoff_notice(resume, load_locale(resume))
    assert notice and "2 cargos" in notice and "2015-01-01" in notice
