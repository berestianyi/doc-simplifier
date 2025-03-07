import re

from contracts.services.dto import BankAccountData, BusinessEntityData


class GeneralFormatter:
    replacements = {
        "обл.": "область",
        "м.": "м.",
        "вул.": "вулиця",
        "буд.": "будинок",
        "кв.": "квартира",
        "офіс": "офіс",
        "с.": "село",
        "смт.": "селище міського типу",
        "р-н": "район",
        "проспект": "проспект",
        "кімната": "кімната"
    }

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


class RoyalFormatter(GeneralFormatter):
    @staticmethod
    def _format_phone(phone: str) -> str:
        if len(phone) != 10 or not phone.isdigit():
            return ""
        return f"38 ({phone[:3]}) {phone[3:6]} {phone[6:8]} {phone[8:]}"

    def _format_bank_data(self, bank: BankAccountData) -> BankAccountData:
        name = self._replace_non_empty_string(bank.get('name'), f"в{bank.get('name')}\n")
        mfo = self._replace_non_empty_string(bank.get('mfo'), f" МФО {bank.get('mfo')}\n")
        iban = self._replace_non_empty_string(bank.get('iban'), f"IBAN {bank.get('iban')}\n")

        return BankAccountData(
            name=name,
            mfo=mfo,
            iban=iban
        )

    def format_entity_data(self, entity: BusinessEntityData) -> BusinessEntityData:
        edrpou = self._replace_non_empty_string(entity.get('edrpou'), f"Код ЄДРПОУ {entity.get('edrpou')}\n")
        address = self._replace_non_empty_string(entity.get('address'), f"Адреса: {entity.get('address')}\n")
        phone = self._replace_non_empty_string(entity.get('phone'),
                                               f"Тел. {self._format_phones(entity.get('phone'))}\n")
        email = self._replace_non_empty_string(entity.get('email'), f"{entity.get('email')}\n")
        bank = self._format_bank_data(entity.get('bank')) if entity.get('bank') else BankAccountData

        result = BusinessEntityData(
            company=entity.get('company'),
            edrpou=edrpou,
            director=entity.get('director'),
            address=address,
            phone=phone,
            email=email,
            pronouns=entity.get('pronouns'),
            bank=bank,
        )
        return result


class RolandFormatter(GeneralFormatter):
    replacements = {
        "обл.": "область",
        "м.": "м.",
        "вул.": "вулиця",
        "буд.": "будинок",
        "кв.": "квартира",
        "офіс": "офіс",
        "с.": "село",
        "смт.": "селище міського типу",
        "р-н": "район",
        "проспект": "проспект",
        "кімната": "кімната"
    }

    @staticmethod
    def _format_phone(phone: str) -> str:
        if len(phone) != 10 or not phone.isdigit():
            return ""
        return f"+38 ({phone[:3]}) {phone[3:6]}-{phone[6:7]}-{phone[7:]}"

    def _format_bank_data(self, bank: BankAccountData) -> BankAccountData:
        name = self._replace_non_empty_string(bank.get('name'), f"в {bank.get('name')},")
        mfo = self._replace_non_empty_string(bank.get('mfo'), f" МФО {bank.get('mfo')}\n")
        iban = self._replace_non_empty_string(bank.get('iban'), f"П/р {bank.get('iban')}\n")
        return BankAccountData(
            name=name,
            mfo=mfo,
            iban=iban
        )

    def format_entity_data(self, entity: BusinessEntityData) -> BusinessEntityData:
        edrpou = self._replace_non_empty_string(entity.get('edrpou'), f"Код ЄДРПОУ {entity.get('edrpou')}\n")

        address = ''
        if self._is_non_empty_string(entity.get('address')):
            address_components = self._replace_address_components(entity.get('address'))
            address = f"Адреса: {address_components}\n"

        phone = self._replace_non_empty_string(entity.get('phone'),
                                               f"Тел. {self._format_phones(entity.get('phone'))}\n")
        email = self._replace_non_empty_string(entity.get('email'), f"Е-mail: {entity.get('email')}\n")

        bank = self._format_bank_data(entity.get('bank'))

        entity_dict = BusinessEntityData(
            company=entity.get('company'),
            edrpou=edrpou,
            director=entity.get('director'),
            address=address,
            phone=phone,
            email=email,
            pronouns=entity.get('pronouns'),
            bank=bank
        )

        return entity_dict
