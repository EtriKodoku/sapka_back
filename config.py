from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    DEBUG: bool = False
    mongo_connection: SecretStr
    resend_connection: SecretStr
    claude_connection: SecretStr
    jwt_secret: SecretStr
    ssl_certfile: str|None = None
    ssl_keyfile: str|None = None
    
    model_config = SettingsConfigDict(env_file=".env")

CONFIG = Settings()