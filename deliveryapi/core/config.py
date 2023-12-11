from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseSettings):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = True


class AuthJWTSettings(BaseSettings):
    jwt_privet_key: Path = BASE_DIR / "certs" / "termokit_api"
    jwt_public_key: Path = BASE_DIR / "certs" / "termokit_api.pub"
    algorithm: str = "RS256"


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    auth: AuthJWTSettings = AuthJWTSettings()


settings = Settings()
