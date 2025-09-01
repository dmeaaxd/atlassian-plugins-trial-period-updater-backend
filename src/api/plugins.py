from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import app_config
from src.database import get_session
from src.models.plugins import PluginModel
from src.schemas.plugins import PluginResponse

plugins_router = APIRouter(tags=["Основная логика получения триальных ключей для плагинов Atlassian"])

@plugins_router.get("/keys", status_code=200, response_model=List[PluginResponse])
async def get_trial_keys(session: Annotated[AsyncSession, Depends(get_session)]):
    result = await session.scalars(select(PluginModel))
    plugins = result.all()

    if not plugins:
        return []

    for plugin in plugins:
        plugin.image_hard_path = f"{app_config.ROOT_PATH}{plugin.image_hard_path}"

    return plugins
    

