import json
import redis.asyncio as redis


class CacheService:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def get(self, key: str) -> dict | None:
        data = await self.redis.get(key)
        if data is None:
            print(f"[CACHE MISS] {key}")
            return None
        print(f"[CACHE HIT] {key}")
        return json.loads(data)

    async def set(self, key: str, value: dict, ttl: int = 86400) -> None:
        await self.redis.setex(key, ttl, json.dumps(value))
        print(f"[CACHE SET] {key} (TTL: {ttl}s)")

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def clear(self) -> None:
        await self.redis.flushdb()
