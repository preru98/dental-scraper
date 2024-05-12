from abc import ABC, abstractmethod
import redis
import json

class Cache(ABC):
    @abstractmethod
    async def add(self, key, value):
        pass

    @abstractmethod
    async def get(self, key):
        pass

class RedisCache(Cache):
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host = host, port= port, db=db)

    async def get(self, key):
        return self.redis_client.get(key)

    async def add(self, key, value):
        return self.redis_client.set(key, value)


async def get_cache() -> Cache:
    return RedisCache()
