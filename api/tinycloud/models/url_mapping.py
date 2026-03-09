from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from datetime import datetime
from ..extensions import db

class UrlMapping(db.Model):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    long_url: Mapped[str] = mapped_column(String, nullable=False)
    short_url: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)