import asyncio
import redis.asyncio as redis

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

async def get_session_state(user_id: str):
    return await redis_client.get(user_id)

async def set_session_state(user_id: str, state: str):
    await redis_client.set(user_id, state)
