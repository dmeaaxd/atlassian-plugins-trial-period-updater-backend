import asyncio

from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base, setup_database


class PluginModel(Base):
    __tablename__ = "plugins"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    image_hard_path: Mapped[str] = mapped_column(nullable=False)
    api_key: Mapped[str] = mapped_column(nullable=False)

# asyncio.run(setup_database())