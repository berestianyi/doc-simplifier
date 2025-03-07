from typing import TypedDict, Optional


class BusinessEntityDTO(TypedDict):
    business_entity: Optional[str]
    edrpou: Optional[str]
    company_name: Optional[str]
    director_name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]
