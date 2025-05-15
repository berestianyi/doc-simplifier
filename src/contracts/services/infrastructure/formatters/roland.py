from src.contracts.services.domain.entities.business_entity import BankAccountData, BusinessEntityData
from src.contracts.services.infrastructure.formatters.general import GeneralFormatter


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
        address = ''
        if self._is_non_empty_string(entity.get('address')):
            address_components = self._replace_address_components(entity.get('address'))
            address = f"Адреса: {address_components}\n"
        edrpou = self._replace_non_empty_string(entity.get('edrpou'), f"Код ЄДРПОУ {entity.get('edrpou')}\n")
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
