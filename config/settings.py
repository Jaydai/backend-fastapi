"""
Application settings and configuration
Centralized configuration management for environment variables and constants
"""
import os
from enum import Enum
import dotenv

dotenv.load_dotenv()


class Environment(str, Enum):
    """Environment types"""
    LOCAL = "local"
    DEV = "dev" # staging
    PROD = "prod"


class BaseSettings:
    """Base settings shared across all environments"""

    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_SECRET_KEY: str = os.getenv("SUPABASE_SECRET_KEY", "")
    SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET", "")

    # App
    APP_VERSION: str = "2.0.0"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", Environment.LOCAL)


class LocalSettings(BaseSettings):
    """Local development settings"""
    
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]


class DevSettings(BaseSettings):
    """Development environment settings"""
    
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "https://app.dev.jayd.ai",
        "chrome-extension://enfcjmbdbldomiobfndablekgdkmcipd",
        "https://chatgpt.com",
        "https://claude.ai",
        "https://chat.mistral.ai",
        "https://copilot.microsoft.com",
        "https://gemini.google.com",
        "https://www.perplexity.ai"
    ]


class ProdSettings(BaseSettings):
    """Production environment settings"""
    
    DEBUG: bool = False
    
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000", # TODO: remove
        "https://app.staging.jayd.ai/", # TODO: remove
        "https://app.jayd.ai",
        "chrome-extension://enfcjmbdbldomiobfndablekgdkmcipd",
        "https://chatgpt.com",
        "https://claude.ai",
        "https://chat.mistral.ai",
        "https://copilot.microsoft.com",
        "https://gemini.google.com",
        "https://www.perplexity.ai"
    ]


def get_settings() -> BaseSettings:
    """Factory function to get settings based on environment"""
    env = os.getenv("ENVIRONMENT", Environment.LOCAL).lower()
    
    settings_map = {
        Environment.LOCAL: LocalSettings,
        Environment.DEV: DevSettings,
        Environment.PROD: ProdSettings,
    }
    
    settings_class = settings_map.get(env, LocalSettings)
    return settings_class()


settings = get_settings()
