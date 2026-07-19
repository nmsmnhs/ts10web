import argparse
import sys
from datetime import datetime, timezone
from typing import get_args

from db import get_session
from generation.pipeline import generate_all
from generation.schemas import Category
from models import Category as CategoryModel, GenerationRun, Question

ALL_CATEGORIES: tuple[str, ...] = get_args(Category)

MODEL_USED = "gemini-2.5-flash"


def get_or_create_categories(session) -> dict[str, int]:
    """Return {category_name: category_id}, inserting any that don't exist yet."""
    existing = {c.name: c.id for c in session.query(CategoryModel).all()}
    for name in ALL_CATEGORIES:
        if name not in existing:
            row = CategoryModel(name=name)
            session.add(row)
            session.flush()  # assigns row.id without committing
            existing[name] = row.id
    return existing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=5, help="Questions per category (default: 5)")
    args = parser.parse_args()

    session = get_session()

    try:
        category_ids = get_or_create_categories(session)

        run = GenerationRun(status="running", model_used=MODEL_USED)
        session.add(run)
        session.flush()  # need run.id before building Question rows

        print(f"Generation run #{run.id} started ({MODEL_USED})")

        results = generate_all(list(ALL_CATEGORIES), args.count)

        total_inserted = total_rejected = 0

        for category, result in results.items():
            for candidate in result.candidates:
                question = Question(
                    category_id=category_ids[category],
                    generation_run_id=run.id,
                    question_type=candidate.question_type,
                    question_text=candidate.question_text,
                    options=candidate.options,
                    correct_answer=candidate.correct_answer,
                )
                session.add(question)
                total_inserted += 1

            total_rejected += len(result.errors)
            print(f"[{category}] {len(result.candidates)} inserted, {len(result.errors)} rejected")
            for err in result.errors:
                print(f"  ! {err}")

        run.status = "completed" if total_rejected == 0 else "completed_with_errors"
        run.completed_at = datetime.now(timezone.utc)

        session.commit()
        print(f"\n=== run #{run.id}: {total_inserted} inserted / {total_rejected} rejected ===")
        return 0

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    sys.exit(main())