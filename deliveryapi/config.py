from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    db_url = ''
    model_config = SettingsConfigDict(env_file="../.env")

    pass
