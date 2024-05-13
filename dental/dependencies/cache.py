from abc import ABC, abstractmethod
import redis
import os
import json

class Cache(ABC):
    @abstractmethod
    async def add(self, key, value):
        pass

    @abstractmethod
    async def get(self, key):
        pass

class RedisCache(Cache):
    def __init__(self, host, port, db):
        self.redis_client = redis.Redis(host = host, port= port, db=db)
        print("Connected to Redis")

    async def get(self, key):
        print("Getting from Redis")
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

    async def add(self, key, value):
        return self.redis_client.set(key, json.dumps(value))


async def get_cache() -> Cache:
    print("Returning cache")
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', '6379'))

    return RedisCache(host = redis_host, port = redis_port, db = 0)
