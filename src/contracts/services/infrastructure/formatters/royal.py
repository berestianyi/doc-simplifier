from src.contracts.services.domain.entities.business_entity import BankAccountData, BusinessEntityData
from src.contracts.services.infrastructure.formatters.general import GeneralFormatter


class RoyalFormatter(GeneralFormatter):
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
