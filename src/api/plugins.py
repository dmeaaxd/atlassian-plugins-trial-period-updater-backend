from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models.plugins import PluginModel

plugins_router = APIRouter(tags=["Основная логика получения триальных ключей для плагинов Atlassian"])
 

@plugins_router.get("/keys", status_code=200)
async def get_trial_keys(session: Annotated[AsyncSession, Depends(get_session)]):
    statement = select(PluginModel)
    
    result = await session.execute(statement)
    plugins = result.scalars().all()
    
    if not plugins:
        return Response(status_code=404, content="No plugin's licences found")
    
    return plugins

