from typing import List

from business_entities.models import BusinessEntities

from contracts.models import Templates
from contracts.services.dto import VehicleData
from contracts.services.interfaces import Converter, Formatter, DocumentEditor


class ContractService:
    def __init__(
            self,
            converter: Converter,
            formatter: Formatter,
            editor: DocumentEditor
    ):
        self.converter = converter
        self.formatter = formatter
        self.editor = editor

    def generate(
            self,
            form_dict,
            start_date,
            end_date,
            entity: BusinessEntities,
            vehicles: List[VehicleData],
            template: Templates,
            contract_id: int
    ) -> tuple[str, str]:

        document_data = self.converter.convert(
            entity,
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
        if vehicles:
            self.editor.add_table(vehicles)

        filename = f"{template.name}_{entity.company_name or entity.director_name}_{contract_id}.docx"
        output = self.editor.save(filename)

        return output, filename
