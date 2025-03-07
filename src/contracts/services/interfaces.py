from typing import Protocol, List, Dict

from business_entities.models import BusinessEntities
from contracts.services.dto import ContractData, BusinessEntityData, VehicleData


class Formatter(Protocol):
    def format_entity_data(self, entity: BusinessEntityData) -> BusinessEntityData: ...

    def flatten_dict(self, d, parent_key='', sep='_') -> dict: ...


class Converter(Protocol):

    def convert(self, entity: BusinessEntities, start_date, expire_date) -> ContractData: ...


class DocumentEditor(Protocol):
    def replace_text(self, replacements: Dict[str, str]): ...

    def add_table(self, data: List[VehicleData]): ...

    def save(self, filename: str) -> str: ...
