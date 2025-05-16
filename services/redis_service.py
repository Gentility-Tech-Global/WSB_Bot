import json
import asyncio
import logging
from redis.asyncio import Redis
from typing import Optional, Union

# Configure logger

logger = logging.getLogger("uvicorn.redis")
logger.setLevel(logging.INFO)

# Redis connection pool
redis_client: Optional[Redis] =None

async def init_redis_pool(
        host: str = "localhost", port: int = 6379, db: int =0, password: Optional[str] = None
):
    """
    Initialize a Redis connection pool
    """

    global redis_client
    redis_client = Redis(host=host, port=port, db=db, password=password, decode_response=True)
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
    :param expire: Expiration in seconds (default: 600)
    """
    try:
        data = json.dumps(value) if isinstance(value, dict) else value
        await redis_client.set(key, data, ex=expire)
        return True
    except Exception as e:
        logger.error(f"Failed to set Redis Key {key}: {e}")
        return False
    

async def get_data(key: str) -> Optional[Union[str, dict]]:
    """
    Retrieve data from Redis. Automatically parses JSON strings into dicts.
    """
    try:
        value = await redis_client.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)  # Try parse JSON
        except json.JSONDecodeError:
            return value  # Return as string
    except Exception as e:
        logger.error(f"Failed to get Redis key {key}: {e}")
        return None


async def delete_data(key: str) -> bool:
    """
    Delete a key from Redis.
    """
    try:
        await redis_client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Failed to delete Redis key {key}: {e}")
        return False


async def exists(key: str) -> bool:
    """
    Check if a key exists in Redis.
    """
    try:
        return await redis_client.exists(key) > 0
    except Exception as e:
        logger.error(f"Redis exists() check failed for key {key}: {e}")
        return False