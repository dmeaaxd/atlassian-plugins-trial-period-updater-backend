import asyncio
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base, setup_database


class PluginModel(Base):
    __tablename__ = "plugins"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    image_hard_path: Mapped[str] = mapped_column(nullable=False)
    api_key: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

# asyncio.run(setup_database())
