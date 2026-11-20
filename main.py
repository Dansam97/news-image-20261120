#!/usr/bin/env python3
"""make.fun entry: news-image-20261120.

"Sum up 20 November's world news in one image."

The front page itself is drawn at build time by draw_page.py (Pillow,
build-time only) and stored here as entry.png. At grading time this
program does the simplest deterministic thing: it copies that baked
image to the output path, byte for byte, with no network and no
randomness, so two runs always produce identical bytes.

Standard library only. The output directory is /output by default,
or $MAKEFUN_OUTPUT_DIR when the harness sets it (local runs).
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def output_path() -> Path:
    """Where the graded image must land.

    The grader runs with a writable /output. Locally the harness
    convention is $MAKEFUN_OUTPUT_DIR, so honour it when set and
    fall back to /output otherwise; either way the file name stays
    entry.png, as the competition requires.
    """
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(base) / "entry.png"


def run() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"missing baked image: {SOURCE}")
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    # copyfile (not copy) so no metadata leaks into the output bytes.
    shutil.copyfile(SOURCE, target)


if __name__ == "__main__":
    run()
