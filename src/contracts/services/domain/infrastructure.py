from abc import ABC, abstractmethod
from typing import List, Dict

from src.business_entities.models import BusinessEntities
from src.contracts.services.domain.entities.business_entity import BusinessEntityData, VehicleData
from src.contracts.services.domain.entities.contract import ContractData


class FormatterInterface(ABC):
    @abstractmethod
    def format_entity_data(self, entity: BusinessEntityData) -> BusinessEntityData:
        raise NotImplementedError

    @abstractmethod
    def flatten_dict(self, d: dict, parent_key: str = '', sep: str = '_') -> dict:
        raise NotImplementedError


class ConverterInterface(ABC):
    @abstractmethod
    def convert(
        self,
        entity: BusinessEntities,
        start_date: str,
        expire_date: str
    ) -> ContractData:
        raise NotImplementedError


class DocumentEditorInterface(ABC):
    @abstractmethod
    def replace_text(self, replacements: Dict[str, str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_table(self, data: List[VehicleData]) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self, filename: str) -> str:
        raise NotImplementedError


# from typing import Protocol, List, Dict
#
# from business_entities.models import BusinessEntities
# from contracts.services.dto import ContractData, BusinessEntityData, VehicleData
#
#
# class Formatter(Protocol):
#     def format_entity_data(self, entity: BusinessEntityData) -> BusinessEntityData: ...
#
#     def flatten_dict(self, d, parent_key='', sep='_') -> dict: ...
#
#
# class Converter(Protocol):
#
#     def convert(self, entity: BusinessEntities, start_date, expire_date) -> ContractData: ...
#
#
# class DocumentEditor(Protocol):
#     def replace_text(self, replacements: Dict[str, str]): ...
#
#     def add_table(self, data: List[VehicleData]): ...
#
#     def save(self, filename: str) -> str: ...
