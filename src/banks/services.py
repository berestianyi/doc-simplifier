from src.business_entities.models import BusinessEntities
from .models import Bank


class BankService:
    def __init__(self, business_entity: BusinessEntities):
        self.business_entity = business_entity

    def add_bank(self, bank: Bank) -> Bank:
        self.business_entity.bank = bank
        self.business_entity.save()
        return self.business_entity.bank

    def add_bank_to_business_entity(self, bank: Bank) -> Bank:
        business_entity = self.business_entity
        if business_entity.bank:
            business_entity.bank = None

        bank = self.add_bank(bank)

        return bank

    def create_bank(self, bank_data) -> Bank:
        bank = Bank.objects.create(**bank_data)
        bank = self.add_bank(bank)
        return bank

    def remove_bank(self) -> None:
        self.business_entity.bank = None
        self.business_entity.save()
        return None
