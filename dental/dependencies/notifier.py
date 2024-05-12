from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    async def notify(self, message):
        pass

class LogNotifier(Notifier):
    def __init__(self):
        pass

    async def notify(self, message):
        print(message)

async def get_notifier() -> Notifier:
    return LogNotifier()