import dotenv
import logging

from typing import Dict, List

env: Dict[str, str] = {}
keys: List[str] = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
]

logger = logging.getLogger(__name__)

def load_env() -> None:
    global env
    if env is not None and len(env) > 0:
        logger.debug("env already loaded")
        return

    for key in keys:
        env[key] = get_key(key)
    logger.debug("env loaded. env=%s", env)

def get_key(key: str) -> str:
    value = dotenv.get_key(".env", key)
    if value is None or value == "":
        raise Exception("%s not found in .env file" % key)
    return value
