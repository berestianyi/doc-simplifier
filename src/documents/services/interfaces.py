from typing import Protocol

from documents.services.dto import BusinessEntityDTO


class Formatter(Protocol):
    def format_entity_data(self, entity: BusinessEntityDTO) -> BusinessEntityDTO: ...


class Extractor(Protocol):
    def extract(self) -> BusinessEntityDTO: ...
