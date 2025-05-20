from typing import List

from src.documents.models import Documents
from src.documents.services.infrastructure.repositories.documents import DocumentRepository
from src.contracts.services.infrastructure.repositories.contracts import ContractRepository
from src.business_entities.models import BusinessEntities
from src.contracts.models import Templates
from src.contracts.services.domain.entities.business_entity import VehicleData
from src.contracts.services.domain.infrastructure import ConverterInterface, DocumentEditorInterface, FormatterInterface
from src.vehicles.models import Vehicles


class GenerateContract:
    def __init__(
            self,
            converter: ConverterInterface,
            formatter: FormatterInterface,
            editor: DocumentEditorInterface
    ):
        self.converter = converter
        self.formatter = formatter
        self.editor = editor
        self.contract_repo = ContractRepository()
        self.document_repo = DocumentRepository()

    def execute(
            self,
            form,
            contract_business_entity: BusinessEntities,
            contract_vehicle_entities: List[Vehicles],
            contract_template: Templates,
    ) -> Documents:
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        created_contract = self.contract_repo.create(
            contract_business_entity=contract_business_entity,
            contract_template=contract_template,
            start_date=start_date,
            end_date=end_date,
        )

        converted_document_data = self.converter.execute(
            contract_business_entity,
            start_date,
            end_date
        )

        replacements = self.formatter.execute(
            converted_document_data,
            form
        )

        filename = f"{contract_template.name}_{contract_business_entity.company_name or contract_business_entity.director_name}_{created_contract.id}.docx"

        output = self.editor.execute(
            replacements,
            self.formatter.format_vehicles_data(contract_vehicle_entities),
            filename
        )

        document = self.document_repo.create(filename=filename, output=output, contract=created_contract)

        return document
