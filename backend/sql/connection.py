import asyncio
import asyncmy
from backend.constants import DB_CONNECT_RETRY_PAUSE, DB_CONNECTION_ATTEMPTS, MIN_POOLS, MAX_POOLS
from config.env_config import settings


class Database:
    pool = None


async def init_db():
    attempts = 0
    while attempts < DB_CONNECTION_ATTEMPTS:
        try:
            Database.pool = await asyncmy.create_pool(
                host=settings.database_hostname,
                port=settings.database_port,
                user=settings.database_username,
                password=settings.database_password,
                db=settings.database_name,
                minsize=MIN_POOLS,  # Minimum number of connections in the pool
                maxsize=MAX_POOLS,  # Maximum number of connections in the pool
            )
            return Database.pool
        except Exception as e:
            print(f"Failed to connect to database. Exception: {e}")
            attempts += 1
            await asyncio.sleep(DB_CONNECT_RETRY_PAUSE)
    raise Exception("Could not connect to the database after max retries")
