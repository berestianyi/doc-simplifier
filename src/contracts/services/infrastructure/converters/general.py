import pymorphy3

from src.business_entities.models import BusinessEntities
from src.contracts.services.domain.entities.contract import ContractData
from src.contracts.services.domain.infrastructure import ConverterInterface

morph = pymorphy3.MorphAnalyzer(lang='uk')


class DataConverter(ConverterInterface):
    MONTH_NAMES_UA = {
        1: "січня",
        2: "лютого",
        3: "березня",
        4: "квітня",
        5: "травня",
        6: "червня",
        7: "липня",
        8: "серпня",
        9: "вересня",
        10: "жовтня",
        11: "листопада",
        12: "грудня",
    }

    @staticmethod
    def _extract_last_name(full_name: str) -> str:
        tokens = full_name.split()
        return tokens[0] if tokens else ""

    @staticmethod
    def _extract_first_name(full_name: str) -> str:
        tokens = full_name.split()
        return tokens[1] if len(tokens) > 1 else ""

    @staticmethod
    def _extract_middle_name(full_name: str) -> str:
        tokens = full_name.split()
        return tokens[2] if len(tokens) > 2 else ""

    @classmethod
    def _to_genitive(cls, full_name: str) -> str:
        tokens = full_name.split()
        result_tokens = []

        for token in tokens:
            parsed = morph.parse(token)
            best_parse = parsed[0]
            gent_form = best_parse.inflect({'gent'})
            if gent_form:
                result_tokens.append(gent_form.word)
            else:
                result_tokens.append(token)
        return " ".join(result_tokens)

    @classmethod
    def _guess_gender_pronoun(cls, name: str) -> str:
        if not name:
            return "що"

        gender_map = {
            "masc": "який",
            "femn": "яка",
        }

        parsed = morph.parse(name)[0]
        return gender_map.get(parsed.tag.gender, "що")

    def _get_document_number(self, start_date, expire_date) -> str:
        return f"{expire_date.day:02d}/{start_date.month}"

    def execute(self, entity: BusinessEntities, start_date, expire_date) -> ContractData:
        return {
            "entity": {
                "company": {
                    "upper": entity.company_name.upper(),
                    "lower": entity.company_name.lower(),
                    "title": entity.company_name.title()
                },
                "edrpou": entity.edrpou,
                "director": {
                    "first_name": {
                        "upper": self._extract_first_name(entity.director_name).upper(),
                        "lower": self._extract_first_name(entity.director_name).lower(),
                        "title": self._extract_first_name(entity.director_name).title()
                    },
                    "last_name": {
                        "upper": self._extract_last_name(entity.director_name).upper(),
                        "lower": self._extract_last_name(entity.director_name).lower(),
                        "title": self._extract_last_name(entity.director_name).title()
                    },
                    "middle_name": {
                        "upper": self._extract_middle_name(entity.director_name).upper(),
                        "lower": self._extract_middle_name(entity.director_name).lower(),
                        "title": self._extract_middle_name(entity.director_name).title()
                    },
                    "full_name": {
                        "upper": entity.director_name.upper(),
                        "lower": entity.director_name.lower(),
                        "title": entity.director_name.title()
                    }
                },
                "pronouns": {
                    "pronoun": self._to_genitive(entity.director_name).upper(),
                    "genitive": self._guess_gender_pronoun(entity.director_name),
                },
                "address": entity.address,
                "phone": entity.phone,
                "email": entity.email,
                "bank": {
                    "name": entity.bank.name if entity.bank else '',
                    "mfo": entity.bank.mfo if entity.bank else '',
                    "iban": entity.iban,
                },
            },
            "date": {
                "start": {
                    "day": f"{start_date.day:02d}",
                    "month": self.MONTH_NAMES_UA[start_date.month],
                    "year": str(start_date.year),
                },
                "end": {
                    "day": f"{expire_date.day:02d}",
                    "month": self.MONTH_NAMES_UA[start_date.month],
                    "year": str(expire_date.year),
                }
            },
            "document":
                {
                    "document_number": self._get_document_number(start_date, expire_date)
                }
        }
