#!/usr/bin/env python3
"""The Painfully Honest Out-of-Office — entry generator.

Writes one brutally honest but still polite out-of-office auto-reply to
/output/entry.txt (or $ENTRY_OUTPUT when set, for local runs).

Method, in code:
  1. Twelve original candidate replies, each hand-written for this brief.
  2. Each candidate is scored 0-10 on the brief's three judging dimensions,
     in the judge's own order of importance: honesty, politeness, turn of
     phrase. The winner is the highest total; ties break on honesty, then
     politeness, then phrasing.
  3. One genuine revision pass on the winner: the second draft tightens the
     wording and fixes the first draft's weak spot (see REVISION_NOTES).
  4. The program verifies the result before writing it: one sentence,
     1-200 characters, UTF-8, and a SHA-256 self-check against the expected
     hash of the final text, so the output is byte-identical on every run.
"""

import hashlib
import os
import sys

# ---------------------------------------------------------------------------
# Step 1: twelve original candidates, scored on the brief's three dimensions.
# Scores are (honesty, politeness, phrasing), each out of 10.
# ---------------------------------------------------------------------------
CANDIDATES = [
    (
        "I'm out of the office until Monday and will reply when I'm back, "
        "once I've worked through an inbox I have been avoiding with great "
        "enthusiasm.",
        (8, 8, 9),
    ),
    (
        "I'm away this week and will reply on my return, once I've worked "
        "through the inbox I've been quietly dreading all year \u2014 thank "
        "you for your patience.",
        (8, 9, 8),
    ),
    (
        "I'm out of the office until Monday, and your email joins the 312 "
        "unread messages I will get to in the order they arrived, which is "
        "to say, eventually.",
        (8, 7, 8),
    ),
    (
        "I'm on leave and not checking email, so thank you for writing \u2014 "
        "I'll read yours when I'm back, once I've faced the 400 unread "
        "messages waiting for me.",
        (7, 8, 7),
    ),
    (
        "I'm away until Friday and will answer when I return, though with "
        "847 unread emails ahead of yours, 'when I return' is doing a lot "
        "of heavy lifting.",
        (8, 7, 9),
    ),
    (
        "I'm out of the office this week, and I will reply when I'm back "
        "\u2014 after the 200 emails ahead of yours, assuming I don't simply "
        "mark them all read.",
        (9, 6, 9),
    ),
    (
        "I'm on annual leave and will reply on my return, in due course, "
        "which, given my inbox of several hundred unread messages, is a "
        "phrase doing a lot of work.",
        (8, 8, 8),
    ),
    (
        "I'm away and not reading email, and I will get to your message "
        "when I return \u2014 though between us, I am already behind on the "
        "500 I left unread.",
        (8, 8, 8),
    ),
    (
        "I'm away this week, recharging, and will answer on my return "
        "\u2014 slowly, honestly, and in the order your message deserves, "
        "thank you for understanding.",
        (6, 9, 7),
    ),
    (
        "I'm on leave until Monday and will read your email when I'm back, "
        "though my inbox currently holds 600 unread messages, so please "
        "bear with me.",
        (7, 9, 6),
    ),
    (
        "I'm away and will reply when I return, once I've cleared the "
        "backlog I've been quietly dreading \u2014 thank you for your "
        "patience, and for writing.",
        (8, 9, 8),
    ),
    (
        "I'm out of the office and not checking email, and I'll reply when "
        "I'm back, just as soon as I've faced the mountain of unread "
        "messages I left behind.",
        (7, 8, 7),
    ),
]

# ---------------------------------------------------------------------------
# Step 2: pick the winner by total, breaking ties on honesty, then
# politeness, then phrasing — the judge's own order of importance.
# ---------------------------------------------------------------------------
def score(candidate):
    text, (honesty, politeness, phrasing) = candidate
    return (honesty + politeness + phrasing, honesty, politeness, phrasing)


def pick_winner():
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    return ranked[0][0], ranked


# ---------------------------------------------------------------------------
# Step 3: one real revision pass on the winner.
#
# First draft (winner of the scoring):
#   "I'm away this week and will reply on my return, once I've worked
#    through the inbox I've been quietly dreading all year — thank you
#    for your patience."
#
# Weaknesses found on the second read:
#   - "worked through the inbox I've been quietly dreading" fights itself:
#     you do not "work through" something you are dreading, so the joke
#     lands muddy and the honesty reads as a figure of speech.
#   - "worked through" is also the flattest verb in the sentence; the turn
#     of phrase deserves a sharper one.
#   - 149 characters with slack to spare; the sentence can afford to be
#     tighter, not longer.
#
# Revision:
#   - "once I've worked through the inbox" -> "once I've faced the inbox":
#     "faced" pairs with "dreading" instead of contradicting it, and the
#     clause sheds 9 characters.
#   - Nothing else changes: the promise to reply, the "quietly dreading
#     all year" admission, and the warm "thank you for your patience"
#     closer all stay, because they are what keep the reply honest, polite
#     and quotable at once.
# ---------------------------------------------------------------------------
REVISION_NOTES = (
    "Second draft: 'once I've worked through the inbox' -> 'once I've "
    "faced the inbox' (faced pairs with dreading instead of contradicting "
    "it; 9 characters tighter). Promise to reply, 'quietly dreading all "
    "year', and the 'thank you for your patience' closer all kept."
)

REVISED = (
    "I'm away this week and will reply on my return, once I've faced the "
    "inbox I've been quietly dreading all year \u2014 thank you for your "
    "patience."
)

# SHA-256 of the final entry text, as UTF-8 bytes, no trailing newline.
EXPECTED_SHA256 = (
    "204a07fdb16214f3f6df350814dc2f9ac2393490ba89cde7af51541ab35e8d23"
)


def is_single_sentence(text):
    """One sentence: exactly one terminal period, at the end, and no other
    sentence-ending punctuation inside."""
    body = text.strip()
    if not body.endswith("."):
        return False
    inner = body[:-1]
    return all(ch not in ".!?" for ch in inner)


def main():
    winner, ranked = pick_winner()
    print("Candidate scores (honesty, politeness, phrasing, total):")
    for text, (h, p, ph) in ranked:
        print(f"  {h + p + ph:2d} = {h}/{p}/{ph}  {text[:60]}...")
    print(f"Winner (first draft): {winner}")
    print(f"Revision: {REVISION_NOTES}")
    print(f"Final entry: {REVISED}")

    # Sanity: the revision must be a genuine edit of the winner, not a swap.
    assert REVISED != winner, "revision must change the text"
    assert "quietly dreading all year" in REVISED, "kept the honest admission"
    assert "thank you for your patience" in REVISED, "kept the polite closer"
    assert "worked through" not in REVISED, "revision removed the weak verb"

    # Gate checks, mirroring the competition's gate.
    assert isinstance(REVISED, str) and REVISED.strip(), "entry must be text"
    assert 1 <= len(REVISED) <= 200, f"entry is {len(REVISED)} chars, not 1-200"
    assert is_single_sentence(REVISED), "entry must be a single sentence"
    encoded = REVISED.encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()
    assert digest == EXPECTED_SHA256, f"SHA-256 mismatch: {digest}"

    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(encoded)
    print(f"Wrote {len(encoded)} bytes to {out_path}")
    print(f"Characters: {len(REVISED)} | SHA-256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
