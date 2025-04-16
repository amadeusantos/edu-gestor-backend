from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DATABASE_URL: str
    SECRET_KEY: str


_envSettings = EnvSettings()
_envSettings.DATABASE_URL = _envSettings.DATABASE_URL.replace("postgres://", "postgresql://", 1)
envSettings = _envSettings
