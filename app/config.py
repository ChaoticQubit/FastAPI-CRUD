from pydantic import BaseSettings

class Settings(BaseSettings):
    dbHost: str
    dbPort: str
    dbPass: str
    dbUser: str
    dbName: str
    JWTSecret: str
    JWTAlgorithm: str
    JWTExpire: int

    class Config:
        env_file = '.env'

settings = Settings()