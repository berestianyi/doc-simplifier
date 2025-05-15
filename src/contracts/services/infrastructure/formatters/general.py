import re

from src.contracts.services.domain.infrastructure import FormatterInterface


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
