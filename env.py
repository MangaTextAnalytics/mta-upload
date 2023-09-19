import dotenv

env = None

def load_env() -> None:
    global env
    if env is not None:
        return env

    db_url = dotenv.get_key(".env", "DB_URL")
    if db_url is None or db_url == "":
        raise Exception("DB_URL not found in .env file")
    env = {
        "db_url": db_url
    }
