from django.db import transaction

from src.contracts.models import Contracts
from src.documents.models import Documents


class DocumentRepository:

    @transaction.atomic
    def create(
            self,
            filename: str,
            output: str,
            contract: Contracts,
    ) -> Documents:

        document = Documents.objects.create(name=filename, path=output, contract=contract)

        return document
