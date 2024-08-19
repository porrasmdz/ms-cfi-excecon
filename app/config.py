from pydantic_settings import BaseSettings, SettingsConfigDict

PRECISION_MULTIPLIER = 100000

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    ENVIRONMENT: str 
    DB_URL : str
    ASYNC_DB_URL : str
    TEST_DB_URL : str 
    DB_SECRET: str 

settings = Settings(_env_file='prod.env', _env_file_encoding='utf-8')