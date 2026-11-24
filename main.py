"""Say What Actually Broke — one honest error line.

The whole entry is a single line of software error copy: the kind of
message a user deserves when a page "goes missing" that never actually
went anywhere. Running this program writes that line, byte for byte,
to entry.txt inside the output directory (MAKEFUN_OUTPUT_DIR when the
environment names one, /output otherwise).
"""

import os
import sys

# The confession itself. One line, no trailing newline: the file is
# exactly this text and nothing else.
CONFESSION = (
    "Error 404 is a lie: this page exists. We renamed it in the redesign "
    "and told nobody \u2014 least of all the links pointing to it. "
    "The search box knows where it lives now."
)

MIN_CHARS = 1
MAX_CHARS = 200


def validate(text):
    """Refuse to ship a line that would fail the gate."""
    if "\n" in text or "\r" in text:
        raise ValueError("the confession must stay on one line")
    if not text.strip():
        raise ValueError("the confession is only whitespace")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "the confession is %d characters; the gate wants %d to %d"
            % (len(text), MIN_CHARS, MAX_CHARS)
        )
    text.encode("utf-8")  # raises if it ever stops being encodable


def target_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def verify_written(path):
    """Read the file back and hold it up against the confession."""
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != CONFESSION.encode("utf-8"):
        raise ValueError("what landed on disk is not the confession")
    validate(on_disk.decode("utf-8"))


def main():
    validate(CONFESSION)
    path = target_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(CONFESSION.encode("utf-8"))
    verify_written(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
