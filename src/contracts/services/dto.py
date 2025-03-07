from typing import TypedDict, Optional


class DocumentInfo(TypedDict):
    document_number: str


class ContractDate(TypedDict):
    day: str
    month: str
    year: str


class ContractDateInfo(TypedDict):
    start: ContractDate
    end: ContractDate


class BankAccountData(TypedDict):
    name: str
    mfo: str
    iban: str


class StrLetterCase(TypedDict):
    upper: str
    lower: str
    title: str


class FullName(TypedDict):
    first_name: StrLetterCase
    last_name: StrLetterCase
    middle_name: StrLetterCase
    full_name: StrLetterCase


class Pronouns(TypedDict):
    genitive: str
    pronoun: str


class BusinessEntityData(TypedDict):
    company: StrLetterCase
    edrpou: str
    director: FullName
    pronouns: Pronouns
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    bank: BankAccountData


class VehicleData(TypedDict):
    brand: str
    model: str
    number: str
    year: int


class ContractData(TypedDict):
    entity: BusinessEntityData
    date: ContractDateInfo
    document: DocumentInfo
