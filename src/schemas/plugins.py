from pydantic import BaseModel


class PluginsSchema(BaseModel):
    name: str
    type: str
    image_hard_path: str
    api_key: str