from abc import ABC, abstractmethod
from src.contracts.services.domain.entities.contract import ContractData


class FormatterInterface(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> dict:
        raise NotImplementedError


class ConverterInterface(ABC):
    @abstractmethod
    def execute(
            self,
            *args, **kwargs
    ) -> ContractData:
        raise NotImplementedError


class DocumentEditorInterface(ABC):
    @abstractmethod
    def execute(
            self,
            *args, **kwargs
    ) -> str:
        raise NotImplementedError
