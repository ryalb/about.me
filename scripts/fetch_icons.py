#!/usr/bin/env python3
"""Refresh the vendored MDI icon subset from the Iconify npm package.

Usage:  mise run icons          (or: python scripts/fetch_icons.py)

Downloads @iconify-json/mdi with `npm pack`, extracts only the icons listed in
WANTED, and rewrites resume_generator/assets/mdi-icons.json.  Browse icon names
at https://icon-sets.iconify.design/mdi/ and add them to WANTED below.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

# semantic name -> MDI icon name (as shown on icon-sets.iconify.design/mdi/)
WANTED = {
    "email": "email-outline",
    "phone": "phone-outline",
    "location": "map-marker-outline",
    "linkedin": "linkedin",
    "github": "github",
    "website": "web",
    "date": "calendar-range-outline",
}

PACKAGE = "@iconify-json/mdi"
_ROOT = Path(__file__).resolve().parents[1]
# Every consumer of the vendored subset: the Python renderers and the JSX theme.
TARGETS = (
    _ROOT / "resume_generator" / "assets" / "mdi-icons.json",
    _ROOT / "custom" / "themes" / "base" / "src" / "mdi-icons.json",
)


def main() -> int:
    if shutil.which("npm") is None:
        print("error: npm is required to fetch icon data", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        print(f"→ npm pack {PACKAGE}")
        proc = subprocess.run(
            ["npm", "pack", PACKAGE, "--silent"],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
            env={
                **dict(__import__("os").environ),
                "npm_config_cache": str(tmpdir / "cache"),
            },
        )
        if proc.returncode != 0:
            print(proc.stderr.strip(), file=sys.stderr)
            return proc.returncode

        tarballs = sorted(tmpdir.glob("*.tgz"))
        if not tarballs:
            print("error: npm pack produced no tarball", file=sys.stderr)
            return 1
        with tarfile.open(tarballs[-1]) as tar:
            tar.extractall(tmpdir, filter="data")

        pkg = tmpdir / "package"
        src = json.loads((pkg / "icons.json").read_text(encoding="utf-8"))
        version = json.loads((pkg / "package.json").read_text(encoding="utf-8"))[
            "version"
        ]
        license_title = json.loads((pkg / "info.json").read_text(encoding="utf-8"))[
            "license"
        ]["title"]

    missing = [n for n in WANTED.values() if n not in src["icons"]]
    if missing:
        print(
            f"error: icons not found in {PACKAGE}: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 1

    out = {
        "_source": PACKAGE,
        "_version": version,
        "_license": license_title,
        "_url": "https://icon-sets.iconify.design/mdi/",
        "_note": "Regenerate with: mise run icons",
        "width": src.get("width", 24),
        "height": src.get("height", 24),
        "icons": {
            key: {"mdi": f"mdi:{name}", "body": src["icons"][name]["body"]}
            for key, name in WANTED.items()
        },
    }
    payload = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    for target in TARGETS:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8")
        print(
            f"✓ wrote {len(out['icons'])} icons to {target.relative_to(_ROOT)} (mdi {version})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
