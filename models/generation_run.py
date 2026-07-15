from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class GenerationRun(Base):
    __tablename__ = "generation_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="running")
    model_used: Mapped[str] = mapped_column(String(100), nullable=False)
    questions: Mapped[list["Question"]] = relationship(back_populates="generation_run")