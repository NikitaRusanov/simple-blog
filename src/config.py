from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.resolve()


class AuthSettings(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    token_expire_minutes: int = 15


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    db_host: str = "127.0.0.1"
    db_port: int = 5432
    db_name: str = "name"
    db_user: str = "user"
    db_pass: str = "pass"

    debug: bool = False

    auth_settings = AuthSettings()


settings = Settings()
