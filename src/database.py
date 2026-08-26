import os
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite:///database.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    pass


async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def migrate():
    """Добавляет недостающие колонки в существующую БД, не трогая данные."""
    def _migrate(conn):
        has_table = conn.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='plugins'"
        ).scalar()
        if not has_table:
            return
        columns = [
            row[1]
            for row in conn.exec_driver_sql("PRAGMA table_info(plugins)").all()
        ]
        if "updated_at" not in columns:
            conn.exec_driver_sql("ALTER TABLE plugins ADD COLUMN updated_at DATETIME")
            mtime = datetime.fromtimestamp(
                os.path.getmtime("database.db"), tz=timezone.utc
            ).replace(tzinfo=None)
            conn.exec_driver_sql(
                "UPDATE plugins SET updated_at = ? WHERE updated_at IS NULL", (mtime,)
            )

    async with engine.begin() as conn:
        await conn.run_sync(_migrate)
