from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from .base import Base

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True, nullable=False)
    generation_run_id: Mapped[int] = mapped_column(ForeignKey("generation_runs.id"), index=True, nullable=False)
    question_type: Mapped[str] = mapped_column(String(20), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[dict | None] = mapped_column(JSONB)
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(768))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    category: Mapped["Category"] = relationship(back_populates="questions")
    generation_run: Mapped["GenerationRun"] = relationship(back_populates="questions")

    __table_args__ = (
        CheckConstraint(
            "(question_type = 'multiple_choice' AND options IS NOT NULL) OR "
            "(question_type = 'true_false' AND options IS NULL)",
            name="ck_question_options_by_type",
        ),
    )