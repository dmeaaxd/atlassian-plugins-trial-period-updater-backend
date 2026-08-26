from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import app_config
from src.database import get_session
from src.models.plugins import PluginModel
from src.schemas.plugins import PluginAdminResponse, PluginCreate, PluginUpdate

admin_router = APIRouter(prefix=app_config.ADMIN_PATH, tags=["Админка"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def require_admin(x_admin_password: Annotated[str | None, Header()] = None):
    if x_admin_password != app_config.ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Неверный пароль")


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


@admin_router.get("")
async def admin_page():
    return FileResponse("src/admin.html")


@admin_router.get(
    "/api/plugins",
    dependencies=[Depends(require_admin)],
    response_model=List[PluginAdminResponse],
)
async def list_plugins(session: SessionDep):
    result = await session.scalars(
        select(PluginModel).order_by(PluginModel.type, PluginModel.name)
    )
    return result.all()


@admin_router.post(
    "/api/plugins",
    dependencies=[Depends(require_admin)],
    response_model=PluginAdminResponse,
)
async def create_plugin(payload: PluginCreate, session: SessionDep):
    plugin = PluginModel(
        name=payload.name,
        type=payload.type.upper(),
        image_hard_path=payload.image_hard_path,
        api_key=payload.api_key,
        updated_at=now_utc(),
    )
    session.add(plugin)
    await session.commit()
    await session.refresh(plugin)
    return plugin


@admin_router.put(
    "/api/plugins/{plugin_id}",
    dependencies=[Depends(require_admin)],
    response_model=PluginAdminResponse,
)
async def update_plugin(plugin_id: int, payload: PluginUpdate, session: SessionDep):
    plugin = await session.get(PluginModel, plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Плагин не найден")
    data = payload.model_dump(exclude_unset=True)
    if "type" in data:
        data["type"] = data["type"].upper()
    for field, value in data.items():
        setattr(plugin, field, value)
    plugin.updated_at = now_utc()
    await session.commit()
    await session.refresh(plugin)
    return plugin


@admin_router.delete(
    "/api/plugins/{plugin_id}",
    dependencies=[Depends(require_admin)],
)
async def delete_plugin(plugin_id: int, session: SessionDep):
    plugin = await session.get(PluginModel, plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Плагин не найден")
    await session.delete(plugin)
    await session.commit()
    return {"ok": True}
