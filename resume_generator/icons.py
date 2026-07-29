"""Inline SVG icons from the Material Design Icons (MDI) Iconify set.

Icon data is vendored in ``assets/mdi-icons.json`` so rendering never needs
network access (WeasyPrint would otherwise have to fetch every icon at PDF
time).  Browse the full set at https://icon-sets.iconify.design/mdi/ and
refresh the vendored subset with ``mise run icons``.

Only monotone MDI icons are used, so ``fill="currentColor"`` in the icon body
makes each icon inherit the surrounding text colour.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_ASSET = Path(__file__).parent / "assets" / "mdi-icons.json"


@lru_cache(maxsize=1)
def _data() -> dict:
    return json.loads(_ASSET.read_text(encoding="utf-8"))


def available() -> list[str]:
    """Return the semantic icon names available (``email``, ``phone``, ...)."""
    return sorted(_data()["icons"])


def mdi_name(name: str) -> str | None:
    """Return the upstream Iconify id for *name* (e.g. ``mdi:email-outline``)."""
    icon = _data()["icons"].get(name)
    return icon["mdi"] if icon else None


def icon_svg(name: str, size: str = "1em", css_class: str = "icon") -> str:
    """Return an inline ``<svg>`` string for the semantic icon *name*.

    Returns an empty string for unknown names so templates degrade quietly
    instead of raising mid-render.
    """
    data = _data()
    icon = data["icons"].get(name)
    if icon is None:
        return ""
    w, h = data["width"], data["height"]
    return (
        f'<svg class="{css_class}" xmlns="http://www.w3.org/2000/svg" '
        f'width="{size}" height="{size}" viewBox="0 0 {w} {h}" '
        f'aria-hidden="true" focusable="false">{icon["body"]}</svg>'
    )
