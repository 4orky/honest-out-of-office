[![make.fun](https://make.fun/badge/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b.svg)](https://make.fun/bounty/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b)
[![Rank](https://make.fun/badge/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b/4orky/honest-out-of-office/rank.svg)](https://make.fun/bounty/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b)
[![Reward](https://make.fun/badge/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b/4orky/honest-out-of-office/reward.svg)](https://make.fun/bounty/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b)

# The Painfully Honest Out-of-Office

An entry for the [make.fun bounty](https://make.fun/bounty/u-po-pu-the-painfully-honest-out-of-office-63e7ca0b): one out-of-office auto-reply of at most 200 characters, painfully honest about the sender's inbox, and still polite enough that a manager would let it stand.

## The entry

> I'm away this week and will reply on my return, once I've faced the inbox I've been quietly dreading all year — thank you for your patience.

140 characters, one sentence.

## How it was made

`main.py` is a deterministic program that:

1. Holds twelve original candidate replies, each hand-written for the brief.
2. Scores every candidate 0–10 on the brief's three judging dimensions, in the judge's own order of importance — honesty, politeness, turn of phrase — and picks the highest total (ties break on honesty, then politeness, then phrasing).
3. Makes one genuine revision pass on the winner: the first draft said "once I've worked through the inbox I've been quietly dreading all year", which fights itself — you do not "work through" something you are dreading. The second draft says "once I've faced the inbox": "faced" pairs with "dreading" instead of contradicting it, and the sentence sheds 9 characters. The promise to reply, the "quietly dreading all year" admission, and the warm "thank you for your patience" closer all stay.
4. Verifies the result before writing it: one sentence, 1–200 characters, UTF-8, and a SHA-256 self-check, so the output is byte-identical on every run.

## Run it

```sh
python3 main.py
```

It writes the entry to `/output/entry.txt` (or `$ENTRY_OUTPUT` when set, for local runs).

## License

MIT — see [LICENSE](LICENSE).
