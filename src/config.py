from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()

class Config(BaseSettings):
    ROOT_PATH: str
    ADMIN_PATH: str = "/admin-x7q2k9"
    ADMIN_PASSWORD: str = "991155"

app_config = Config()
