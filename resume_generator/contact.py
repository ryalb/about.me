"""Contact-line helpers shared by the renderers."""

from __future__ import annotations

import re
from typing import Any

_SCHEME = re.compile(r"^[a-z][a-z0-9+.\-]*://", re.IGNORECASE)


def profile_display(profile: dict[str, Any]) -> str:
    """Return the visible text for a ``basics.profiles`` entry.

    Prefers the profile URL with its scheme and trailing slash removed
    (``linkedin.com/in/ryalb``).  ATS parsers and ``pdftotext`` read the
    *rendered* text, so a bare username leaves no way back to the profile —
    the href alone is invisible to them.  Falls back to ``network: username``
    when the entry records no URL.
    """
    url = (profile.get("url") or "").strip()
    if url:
        return _SCHEME.sub("", url).rstrip("/")

    network = (profile.get("network") or "").strip()
    username = (profile.get("username") or "").strip()
    if network and username:
        return f"{network}: {username}"
    return username or network
