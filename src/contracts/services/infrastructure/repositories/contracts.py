from django.db import transaction

from src.contracts.services.domain.repository import ContractRepositoryInterface
from src.business_entities.models import BusinessEntities
from src.contracts.models import Templates
from src.contracts.models import Contracts


class ContractRepository(ContractRepositoryInterface):

    @transaction.atomic
    def create(
            self,
            contract_business_entity: BusinessEntities,
            contract_template: Templates,
            start_date,
            end_date
    ) -> Contracts:

        contract = Contracts.objects.create(
            business_entities=contract_business_entity,
            template=contract_template,
            start_date=start_date,
            end_date=end_date,
        )

        return contract

    def get_by_id(self, contract_id: int):
        try:
            return Contracts.objects.get(id=contract_id)
        except Contracts.DoesNotExist:
            return None

    def list(self):
        return Contracts.objects.all()
