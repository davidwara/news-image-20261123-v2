#!/usr/bin/env python3
"""World in a Day — make.fun news-image-20261123 entrypoint.

Copies the pre-rendered front page (entry.png, 1024x1024, the world's news
of Monday 23 November 2026) to the output directory as entry.png.

Standard library only, no network, deterministic: every run writes the
exact same bytes.
"""

import os
import sys

IMAGE_NAME = "entry.png"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, IMAGE_NAME)

    with open(source, "rb") as fh:
        data = fh.read()

    # Sanity check: the payload must be a whole PNG (magic bytes + IEND).
    if not data.startswith(b"\x89PNG\r\n\x1a\n") or not data.endswith(b"IEND\xaeB`\x82"):
        print("error: source is not a complete PNG file", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(target, "wb") as fh:
        fh.write(data)

    with open(target, "rb") as fh:
        written = fh.read()
    if written != data:
        print("error: output bytes differ from source", file=sys.stderr)
        return 1

    print(f"wrote {target} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
