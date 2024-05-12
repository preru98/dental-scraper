from abc import ABC, abstractmethod
import json

class Store(ABC):
    @abstractmethod
    async def insert(self, values):
        pass

    @abstractmethod
    async def update(self, docs):
        pass

    @abstractmethod
    async def get_all(self):
        pass

class JSONStore(Store):
    def __init__(self, filepath: str):
        self.filepath = filepath

    async def get(self, key: str):
        with open(self.filepath, 'r') as file:
            data = json.load(file)
            return data.get(key)

    async def update(self, docs):
        with open(self.filepath, 'w') as file:
            data = json.load(file)
            for doc in docs:
                data[doc['key']] = doc['value']
            json.dump(data, file)

    async def get_all(self):
        with open(self.filepath, 'r') as file:
            return json.load(file)

async def get_store() -> Store:
    return JSONStore(filepath='data.json')