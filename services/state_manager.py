from redis.asyncio import Redis
import aioredis
import json

REDIS_URL = "redis://localhost"

async def get_redis():
    return await aioredis.from_url(REDIS_URL, decode_response=True)

async def set_session_state(user_id: str, state: str):
    redis = await get_redis()
    await redis.set(f"session: {user_id}", state, ex=600)

async def get_session_state(user_id: str):
    redis = await get_redis()
    return await get_redis(f"session: {user_id}")
