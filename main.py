#!/usr/bin/env python3
"""One line to send back to a younger self.

The program writes a single English sentence — the line its author would
send to their younger self — into entry.txt under the output directory the
grader provides. The line is fixed: it is the author's own, not generated
at run time, so the two runs the grader does produce the same file.

Output rules, from the competition gate:
  * entry.txt must hold UTF-8 text, 1 to 200 characters;
  * it must not be only whitespace;
  * it must be one line, no line breaks.

The output directory comes from MAKEFUN_OUTPUT_DIR when that variable is
set, and defaults to /output. Nothing is read from or written to the
current working directory, and only the standard library is used.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# The line itself: a warning to the author's younger self about a leather
# jacket bought to impress a girl who would leave him anyway — a mistake
# still being paid off at thirty.
MESSAGE = (
    "Don't buy the leather jacket to impress her — "
    "she leaves you for the boy in the hoodie, "
    "and you'll still be paying off that jacket at thirty."
)

MAX_CHARS = 200


def output_dir() -> Path:
    """Where entry.txt goes: the env var, or /output as a fallback."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def checked(message: str) -> str:
    """Return the message only if it fits the gate, else stop loudly.

    Edge whitespace is refused rather than trimmed: the stored line
    must be exactly the author's line, byte for byte.
    """
    if message != message.strip():
        sys.exit("refusing to write an entry with edge whitespace")
    if not message:
        sys.exit("refusing to write an empty entry")
    if "\n" in message or "\r" in message:
        sys.exit("entry must be a single line")
    if len(message) > MAX_CHARS:
        sys.exit(f"entry is {len(message)} chars, over the {MAX_CHARS} limit")
    return message


def main() -> int:
    text = checked(MESSAGE)
    folder = output_dir()
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.txt"
    target.write_text(text, encoding="utf-8")
    # Read it back and compare, so a partial write cannot pass silently.
    if target.read_text(encoding="utf-8") != text:
        sys.exit("entry.txt did not round-trip")
    print(f"wrote {len(text)} chars to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
