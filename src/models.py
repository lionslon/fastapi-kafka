from datetime import datetime
from typing import Any

from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()


class DataEntry(Base):
    __tablename__ = "data_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[dict[str, Any]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self) -> str:
        return f"DataEntry(id={self.id})"
