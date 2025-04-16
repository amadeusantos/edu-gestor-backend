from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DATABASE_URL: str
    SECRET_KEY: str


envSettings = EnvSettings()
