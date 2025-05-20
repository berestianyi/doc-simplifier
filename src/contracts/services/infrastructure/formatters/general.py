import re
from typing import List

from src.contracts.services.domain.entities.business_entity import VehicleData
from src.contracts.services.domain.infrastructure import FormatterInterface
from src.vehicles.models import Vehicles


class GeneralFormatter(FormatterInterface):
    replacements = {}

    def _replace_address_components(self, address: str) -> str:
        pattern = re.compile(r'\b(' + '|'.join(map(re.escape, self.replacements.keys())) + r')\b')
        return pattern.sub(lambda x: self.replacements[x.group()], address)

    @staticmethod
    def _is_non_empty_string(value):
        return isinstance(value, str) and bool(value.strip())

    def _replace_non_empty_string(self, value, replace: str) -> str:

        is_not_empty = self._is_non_empty_string(value)

        if is_not_empty:
            return replace
        return ''

    @staticmethod
    def _format_phone(phone: str) -> str:
        digits = "".join(ch for ch in phone if ch.isdigit())
        if digits.startswith("380") and len(digits) >= 11:
            phone = digits[2:]
            return phone
        return ""

    def _format_phones(self, phones: str) -> str:
        phones = re.split(r"[,\s]+", phones.strip())
        results = []

        for phone in phones:
            if not phone:
                continue
            royal_phone = self._format_phone(phone)
            if royal_phone:
                results.append(royal_phone)
            else:
                results.append(phone)

        return ", ".join(results)

    def flatten_dict(self, d: dict, parent_key: str = '', sep: str = '_') -> dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def format_vehicles_data(self, vehicles: List[Vehicles]) -> List[VehicleData]:
        vehicles_data_list = []
        for vehicle in vehicles:
            vehicle_data = VehicleData(
                brand=vehicle.brand,
                model=str(vehicle.model),
                number=vehicle.number,
                year=int(vehicle.year),
            )
            vehicles_data_list.append(vehicle_data)

        return vehicles_data_list


    def execute(self, converted_document_data: dict, form):

        form_dict = {
            field: dict(form.fields[field].choices).get(value, value)
            for field, value in form.cleaned_data.items()
            if field in form.fields and hasattr(form.fields[field], "choices")
        }

        formatted_entity = self.format_entity_data(converted_document_data['entity'])

        flattened_entity_data = self.flatten_dict(formatted_entity)
        flattened_date_data = self.flatten_dict(converted_document_data['date'])
        flattened_document_data = self.flatten_dict(converted_document_data['document'])
        replacements = {
            **form_dict,
            **flattened_entity_data,
            **flattened_date_data,
            **flattened_document_data
        }

        return replacements

