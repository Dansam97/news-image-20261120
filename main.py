#!/usr/bin/env python3
"""make.fun entry: news-image-20261120.

Behaviour: put the pre-baked front page (entry.png, rendered ahead of
time by draw_page.py) where the grader expects it. The transfer is a
plain byte copy -- nothing is decoded, fetched or randomised -- so
every run yields exactly the same output file. Standard library only.
"""

import os
from pathlib import Path

BAKED_PAGE = Path(__file__).resolve().with_name("entry.png")


def destination() -> Path:
    """Output location: $MAKEFUN_OUTPUT_DIR when set, else /output."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(folder) / "entry.png"


def main() -> None:
    if not BAKED_PAGE.is_file():
        raise SystemExit("baked front page is missing: %s" % BAKED_PAGE)
    target = destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(BAKED_PAGE.read_bytes())


if __name__ == "__main__":
    main()
