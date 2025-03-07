import re

from documents.services.dto import BusinessEntityDTO


class BusinessEntityDataFormatter:
    @staticmethod
    def _address_formatter(text: str) -> str:
        replacement_patterns = [
            (r"(місто|м\.)", "м."),
            (r"(вулиця|вул\.|в\.)", "вул."),
            (r"(район|р-н|р\.)", "р-н"),
            (r"(область|обл\.)", "обл."),
            (r"(смт)", "с."),
            (r"(будинок|буд\.)", "буд."),
            (r"(квартира|кв\.)", "кв.")
        ]

        text_without_country = re.sub(r'\bУкраїна,\s*', '', text)
        text_without_duplicate_index = re.sub(r'\s+', ' ', text_without_country)

        replaced_text = text_without_duplicate_index.title()

        for pattern, replacement in replacement_patterns:
            replaced_text = re.sub(
                fr"\b{pattern}\b",
                replacement,
                replaced_text,
                flags=re.IGNORECASE
            )

        return replaced_text

    @staticmethod
    def _phone_formatter(phone_number: str) -> str:
        phone_number_list = phone_number.strip().split(',')
        cleaned_numbers = []
        for number in phone_number_list:
            cleaned_number = re.sub(r'[^\d]', '', number)
            cleaned_number = cleaned_number.lstrip('38')
            cleaned_numbers.append(cleaned_number)

        return ", ".join(cleaned_numbers)

    def format_entity_data(self, entity: BusinessEntityDTO) -> BusinessEntityDTO:
        return {
            'business_entity': entity['business_entity'],
            'edrpou': entity['edrpou'],
            'company_name': entity.get('company_name'),
            'director_name': entity['director_name'].title(),
            'address': self._address_formatter(entity['address']),
            'phone': self._phone_formatter(entity.get('phone', '')),
            'email': entity.get('email', '').lower()
        }
