"""
Settings module
"""
from os import getenv
from pathlib import Path

import environ

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

env_name = getenv("POPREPO_SETTINGS_ENV", "dev")
env = environ.Env()
env.read_env(ROOT_DIR / f"env/.env.{env_name}")


class Settings:
    """App settings"""

    POPREPO_LOG_LEVEL: str = env.str("POPREPO_LOG_LEVEL", default="error")
    POPREPO_LIVE_RELOAD: bool = env.bool("POPREPO_LIVE_RELOAD", default=False)

    POPREPO_REDIS_HOST: str = env.str("POPREPO_REDIS_HOST", default="localhost")
    POPREPO_REDIS_PORT: int = env.int("POPREPO_REDIS_PORT", default=6379)
    POPREPO_REDIS_PASSWORD: str = env.str("POPREPO_REDIS_PASSWORD", default="")

    POPREPO_FEATURE_CACHE_ENABLED: bool = env.bool(
        "POPREPO_FEATURE_CACHE_ENABLED", default=True
    )
    POPREPO_FEATURE_CACHE_TTL_SEC: str = env.str(
        "POPREPO_FEATURE_CACHE_TTL_SEC", default=86400
    )
    POPREPO_FEATURE_CACHE_ENDPOINTS: list = env.list(
        "POPREPO_FEATURE_CACHE_ENDPOINTS", default=[]
    )
