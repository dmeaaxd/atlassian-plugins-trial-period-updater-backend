from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()

class Config(BaseSettings):
    ROOT_PATH: str

app_config = Config()

