# Interface for command executors

from abc import ABC, abstractmethod

from db_adapters.adapter import Adapter


class CommandExecutor(ABC):
    @abstractmethod
    def execute(self, database_adapter: Adapter, parameters: list[str]) -> dict:
        pass
