from typing import Annotated, List

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models.plugins import PluginModel
from src.schemas.plugins import PluginsSchema

plugins_router = APIRouter(tags=["Основная логика получения триальных ключей для плагинов Atlassian"])
 

@plugins_router.get("/keys", status_code=200, response_model=List[PluginsSchema])
async def get_trial_keys(session: Annotated[AsyncSession, Depends(get_session)]):
    statement = select(PluginModel)
    
    result = await session.execute(statement)
    plugins = result.scalars().all()

    if not plugins:
        return []

    return plugins
    

