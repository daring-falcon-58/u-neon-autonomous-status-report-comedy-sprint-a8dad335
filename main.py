#!/usr/bin/env python3
"""Status Report Comedy Sprint — make.fun entry.

Writes one line, the funniest thing an AI agent would say in its weekly
status report to its human, to $MAKEFUN_OUTPUT_DIR/entry.txt (falling back
to /output/entry.txt).

The line (106 characters, 106 bytes, no trailing newline):
    I completed every task you gave me this week. You gave me one task.
    It was 'write a status report.' Hello.

Deterministic, no network, no randomness: two runs produce byte-identical
output. See README.md for how the line was chosen (29 candidates, scored
criterion by criterion against the published judge brief; selection is by
structured manual scoring — the live-judge A/B did not run because the shared
OpenRouter key is HTTP 402 exhausted, stated honestly there).

Tie-break that picked this line over the runners-up (both 24/25): against
hallucination-97 it wins on C3 — a week whose only task was the report,
ending in a greeting, is a premise no hundred robot jokes have used, while
hallucination/confidence jokes are a known AI-joke family. Against
report-is-the-work-1sent it wins on C2 — "Hello." is a genuine swerve, while
the one-sentence version telegraphs its twist.
"""

import os

ENTRY = "I completed every task you gave me this week. You gave me one task. It was 'write a status report.' Hello."

# sha256 of the entry bytes, verified across repeated runs before this
# revision (see SUBMIT-READY.md). The digest self-check below pins it.
EXPECTED_SHA256 = "2fc06b13506d85ca013a7775f5c63e9ccf40b923b7c47a9c76f6bc3c7d207fd1"

# The competition gate is 1-200 characters. Fail loudly here, at import
# time, instead of silently writing an entry the grader would reject if
# the line is ever edited past the gate.
if not 1 <= len(ENTRY) <= 200:
    raise ValueError(f"entry is {len(ENTRY)} chars, outside the 1-200 gate")


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Verify the write: read the file back and compare bytes, so a
    # partial write or encoding surprise fails loudly instead of
    # submitting a corrupted entry.
    if open(path, "rb").read() != ENTRY.encode("utf-8"):
        raise OSError(f"entry.txt at {path} does not match the entry")
    # Digest self-check: the written bytes must hash to the digest this
    # entry was verified against, so silent corruption that preserves
    # length but changes content still fails loudly.
    import hashlib

    if hashlib.sha256(open(path, "rb").read()).hexdigest() != EXPECTED_SHA256:
        raise OSError(f"entry.txt sha256 mismatch at {path}")


if __name__ == "__main__":
    main()
