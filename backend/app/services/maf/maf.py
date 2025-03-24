from abc import ABC, abstractmethod


class MultiAgentFramework(ABC):
    @abstractmethod
    async def start_task(self, *args, **kwargs):
        pass
