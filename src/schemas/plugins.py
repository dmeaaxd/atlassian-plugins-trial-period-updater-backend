from pydantic import BaseModel


class PluginResponse(BaseModel):
    name: str
    type: str
    image_hard_path: str
    api_key: str


    class Config:
        from_attributes = True