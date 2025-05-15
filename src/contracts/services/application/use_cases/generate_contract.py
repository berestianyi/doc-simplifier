from typing import List

from src.business_entities.models import BusinessEntities
from src.contracts.models import Templates
from src.contracts.services.domain.entities.business_entity import VehicleData
from src.contracts.services.domain.infrastructure import ConverterInterface, DocumentEditorInterface, FormatterInterface


class ContractService:
    def __init__(
            self,
            converter: ConverterInterface,
            formatter: FormatterInterface,
            editor: DocumentEditorInterface
    ):
        self.converter = converter
        self.formatter = formatter
        self.editor = editor

    def execute(
            self,
            form_dict,
            start_date,
            end_date,
            entity_model: BusinessEntities,
            vehicle_entities: List[VehicleData],
            template_model: Templates,
            contract_id: int
    ) -> tuple[str, str]:

        document_data = self.converter.convert(
            entity_model,
            start_date,
            end_date
        )

        formatted_entity = self.formatter.format_entity_data(document_data['entity'])

        flattened_entity_data = self.formatter.flatten_dict(formatted_entity)
        flattened_date_data = self.formatter.flatten_dict(document_data['date'])
        flattened_document_data = self.formatter.flatten_dict(document_data['document'])
        replacements = {
            **form_dict,
            **flattened_entity_data,
            **flattened_date_data,
            **flattened_document_data
        }
        print(replacements)
        self.editor.replace_text(replacements)
        if vehicle_entities:
            self.editor.add_table(vehicle_entities)

        filename = f"{template_model.name}_{entity_model.company_name or entity_model.director_name}_{contract_id}.docx"
        output = self.editor.save(filename)

        return output, filename
