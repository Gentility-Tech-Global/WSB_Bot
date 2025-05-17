import json
import asyncio
import logging
from redis.asyncio import Redis
from typing import Optional, Union

# Configure logger
logger = logging.getLogger("uvicorn.redis")
logger.setLevel(logging.INFO)

# Redis client
redis_client: Optional[Redis] = None

async def init_redis_pool(
    host: str = "localhost",
    port: int = 6379,
    db: int = 0,
    password: Optional[str] = None
) -> Redis:
    """
    Initialize a Redis connection pool and assign it to the global redis_client.
    :param host: Redis server host
    :param port: Redis server port
    :param db: Redis database number
    :param password: Redis password
    :return: Redis client instance
    """
    global redis_client
    redis_client = Redis(
        host=host,
        port=port,
        db=db,
        password=password,
        decode_responses=True
    )
    try:
        await redis_client.ping()
        logger.info("✅ Connected to Redis")
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")
        raise

async def set_data(key: str, value: Union[str, dict], expire: int = 600) -> bool:
    """
    Store data in Redis. Automatically serializes dict to JSON.
    :param key: Redis key
    :param value: Data to store (string or dict)
    :param expire: Expiration time in seconds
    """
    try:
        data = json.dumps(value) if isinstance(value, dict) else value
        await redis_client.set(key, data, ex=expire)
        return True
    except Exception as e:
        logger.error(f"❌ Failed to set Redis key '{key}': {e}")
        return False

async def get_data(key: str) -> Optional[Union[str, dict]]:
    """
    Retrieve data from Redis. Automatically parses JSON strings into dicts.
    :param key: Redis key
    :return: Stored value (dict, string, or None)
    """
    try:
        value = await redis_client.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    except Exception as e:
        logger.error(f"❌ Failed to get Redis key '{key}': {e}")
        return None

async def delete_data(key: str) -> bool:
    """
    Delete a key from Redis.
    :param key: Redis key
    :return: Success status
    """
    try:
        await redis_client.delete(key)
        return True
    except Exception as e:
        logger.error(f"❌ Failed to delete Redis key '{key}': {e}")
        return False

async def exists(key: str) -> bool:
    """
    Check if a key exists in Redis.
    :param key: Redis key
    :return: True if key exists, False otherwise
    """
    try:
        return await redis_client.exists(key) > 0
    except Exception as e:
        logger.error(f"❌ Redis exists() check failed for key '{key}': {e}")
        return False
