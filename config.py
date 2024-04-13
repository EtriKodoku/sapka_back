from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    DEBUG: bool = False
    mongo_connection: SecretStr
    resend_connection: SecretStr
    
    model_config = SettingsConfigDict(env_file=".env")

CONFIG = Settings()