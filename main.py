#!/usr/bin/env python3
"""One line to my younger self.

This program exists for one job: put a single fixed line into
``entry.txt`` inside the grader's output directory, so the judge can
read it. The line never changes between runs — it is the author's own
words, written once here, and the program only checks it against the
competition gate before writing it out.

Gate (from the competition rules):
  * entry.txt is UTF-8 text, 1 to 200 characters;
  * it is not only whitespace;
  * it is a single line (no newline characters).

The output directory is taken from the MAKEFUN_OUTPUT_DIR environment
variable when it is set, and falls back to /output. Nothing is read
from the current working directory, nothing is written there, and the
program uses only the Python standard library.
"""

import os
import sys
from pathlib import Path

# The author's line, word for word. It warns the younger self about a
# leather jacket bought to impress a girl who leaves him for the boy
# in the hoodie — a purchase he is still paying off at thirty.
LINE = (
    "Don't buy the leather jacket to impress her — "
    "she leaves you for the boy in the hoodie, "
    "and you'll still be paying off that jacket at thirty."
)

# The gate's upper bound on the entry's length, in characters.
LIMIT = 200


def pick_output_dir() -> Path:
    """Return the directory entry.txt belongs in."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if chosen:
        return Path(chosen)
    return Path("/output")


def gate(line: str) -> None:
    """Stop with an error unless the line passes the gate as-is.

    The line is never trimmed or reworded here: if it does not fit
    the gate exactly as written, the program refuses to write it,
    rather than silently changing the author's words.
    """
    if not line:
        sys.exit("entry is empty")
    if line.strip() == "":
        sys.exit("entry is only whitespace")
    if line != line.strip():
        sys.exit("entry has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        sys.exit("entry spans more than one line")
    # Unicode line/paragraph separators and vertical whitespace would
    # also split the entry into more than one line for a reader, even
    # though they are not \n or \r.
    for bad in ("\u2028", "\u2029", "\x0b", "\x0c"):
        if bad in line:
            sys.exit("entry contains a line-breaking character")
    if len(line) > LIMIT:
        sys.exit(f"entry is {len(line)} chars, over the {LIMIT} limit")


def write_entry() -> int:
    gate(LINE)
    out_dir = pick_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    entry_file = out_dir / "entry.txt"
    entry_file.write_text(LINE, encoding="utf-8")
    # Read the file back and check it matches, so a truncated or
    # partial write is caught instead of passing silently.
    if entry_file.read_text(encoding="utf-8") != LINE:
        sys.exit("entry.txt does not match the line after writing")
    print(f"wrote {len(LINE)} chars to {entry_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(write_entry())
