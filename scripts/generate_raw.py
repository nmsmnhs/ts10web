import argparse
import sys
from typing import get_args

from generation.pipeline import generate_for_category, generate_all
from generation.schemas import Category, QuestionCandidate

ALL_CATEGORIES: tuple[str, ...] = get_args(Category)


def _print_candidate(i: int, candidate: QuestionCandidate) -> None:
    print(f"  --- candidate {i} ---")
    print(f"  {candidate.model_dump_json(indent=2)}")


def _print_result(category: str, result) -> tuple[int, int]:
    print(f"\n[{category}] {len(result.candidates)} valid, {len(result.errors)} rejected")
    for i, candidate in enumerate(result.candidates, start=1):
        _print_candidate(i, candidate)
    for err in result.errors:
        print(f"  ! {err}")
    return len(result.candidates), len(result.errors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--category", choices=ALL_CATEGORIES, help="Generate for a single category")
    target.add_argument("--all", action="store_true", help="Generate for all 8 categories")
    parser.add_argument("--count", type=int, default=5, help="Questions per category (default: 5)")
    args = parser.parse_args()

    total_valid = total_rejected = 0

    if args.all:
        results = generate_all(list(ALL_CATEGORIES), args.count)
        for category, result in results.items():
            valid, rejected = _print_result(category, result)
            total_valid += valid
            total_rejected += rejected
    else:
        result = generate_for_category(args.category, args.count)
        total_valid, total_rejected = _print_result(args.category, result)

    print(f"\n=== {total_valid} valid / {total_rejected} rejected ===")
    return 0 if total_rejected == 0 else 1


if __name__ == "__main__":
    sys.exit(main())