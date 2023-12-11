from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env')

    db_host: str = '127.0.0.1'
    db_port: int = 5432
    db_name: str = 'name'
    db_user: str = 'user'
    db_pass: str = 'pass'


settings = Settings()