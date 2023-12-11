from datetime import timedelta
from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseSettings):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = True


class SuperUserSettings(BaseSettings):
    name: str = "superuser"
    password: str = "superuser"


class AuthJWTSettings(BaseSettings):
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "RS256"
    access_token_expires_delta: timedelta = timedelta(minutes=15)


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    auth: AuthJWTSettings = AuthJWTSettings()
    superuser: SuperUserSettings = SuperUserSettings()


settings = Settings()
