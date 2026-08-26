from datetime import datetime

from pydantic import BaseModel


class PluginResponse(BaseModel):
    name: str
    type: str
    image_hard_path: str
    api_key: str
    updated_at: datetime | None


    class Config:
        from_attributes = True


class PluginAdminResponse(PluginResponse):
    id: int
    updated_at: datetime | None


class PluginCreate(BaseModel):
    name: str
    type: str
    image_hard_path: str
    api_key: str


class PluginUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    image_hard_path: str | None = None
    api_key: str | None = None
