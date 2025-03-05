from abc import ABC, abstractmethod


class MultiAgentFramework(ABC):
    @abstractmethod
    def start_task(self, *args, **kwargs):
        pass
