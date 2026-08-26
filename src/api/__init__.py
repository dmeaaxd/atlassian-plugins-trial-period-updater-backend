from fastapi import APIRouter

from src.api.admin import admin_router
from src.api.plugins import plugins_router


main_router = APIRouter()
main_router.include_router(plugins_router)
main_router.include_router(admin_router)
