"""Conservative cleanup for common Indonesian speech-to-text fillers."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from typing import Iterable


FILLER_PATTERN = re.compile(
    r"(?<!\w)(?:(?P<eee>e{2,})|(?P<em>em+)|(?P<anu>anu))(?!\w)",
    re.IGNORECASE,
)


def clean_transcript(text: str) -> tuple[str, dict[str, int]]:
    """Remove only common standalone hesitation tokens and tidy nearby spacing.

    Meaningful interjections such as ``eh`` and ``hmm`` are intentionally kept.
    The function does not add punctuation, rewrite words, or correct grammar.
    """
    counts: Counter[str] = Counter()

    def remove_filler(match: re.Match[str]) -> str:
        category = match.lastgroup or "unknown"
        counts[category] += 1
        return ""

    cleaned = FILLER_PATTERN.sub(remove_filler, text)
    # Remove punctuation orphaned at the beginning of a line, tidy spaces around
    # punctuation, and collapse duplicates left when a filler sat between commas.
    cleaned = re.sub(r"(?m)^[ \t]*[,;:.!?]+[ \t]*", "", cleaned)
    cleaned = re.sub(r"[ \t]+([,;:.!?])", r"\1", cleaned)
    cleaned = re.sub(r"([,;:])(?:[ \t]*[,;:])+", r"\1", cleaned)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"(?m)^[ \t]+|[ \t]+$", "", cleaned)
    return cleaned, dict(sorted(counts.items()))


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="rapi-transkrip-id",
        description="Hapus kata jeda yang umum dari transkrip Indonesia, tanpa API.",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="tampilkan jumlah kata jeda yang dihapus di stderr",
    )
    args = parser.parse_args(argv)

    source = sys.stdin.read()
    result, counts = clean_transcript(source)
    sys.stdout.write(result)
    if result and not result.endswith("\n"):
        sys.stdout.write("\n")

    if args.stats and counts:
        summary = ", ".join(f"{category}={count}" for category, count in counts.items())
        total = sum(counts.values())
        print(f"rapi-transkrip-id: menghapus {total} kata jeda ({summary}).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
