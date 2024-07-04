from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "dev"
    app_name: str = "Automatico-Automation"
    POSTGRES_URL_NON_POOLING: str
    POSTGRES_PRISMA_URL: str
    auth_secret: str

    model_config = SettingsConfigDict(env_file=".env")
