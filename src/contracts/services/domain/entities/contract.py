from typing import TypedDict

from src.contracts.services.domain.entities.business_entity import BusinessEntityData


class DocumentInfo(TypedDict):
    document_number: str


class ContractDate(TypedDict):
    day: str
    month: str
    year: str


class ContractDateInfo(TypedDict):
    start: ContractDate
    end: ContractDate


class ContractData(TypedDict):
    entity: BusinessEntityData
    date: ContractDateInfo
    document: DocumentInfo
