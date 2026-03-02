from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Brindimarket"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/brindimarket"
    
    # Security
    SECRET_KEY: str = "super-secret-key-change-it-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Telebirr (Placeholders)
    TELEBIRR_BASE_URL: str = ""
    TELEBIRR_FABRIC_APP_ID: str = ""
    TELEBIRR_APP_SECRET: str = ""
    TELEBIRR_MERCHANT_APP_ID: str = ""
    TELEBIRR_MERCHANT_CODE: str = ""
    TELEBIRR_PRIVATE_KEY: str = ""
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
