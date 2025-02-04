import re

import PyPDF2


class TextExtraction:
    fop_regex_dict = {
        'director_name': r'ФОП\s+(.+?)\s+Витяг з Єдиного державного реєстру юридичних осіб',
        'edrpou': r'Ідентифікаційний код:\s*(\d+)\s*Адреса:',
        'address': r'Адреса:\s*(.+?)\s*Статус:',
        'phone': r'Контактна інформація\s*Телефони:\s*(.+?)\s*(Email:.*|Дані про взяття на облік)',
        'email': r'Контактна інформація\s*Телефони:\s*.+?\s*Email:\s*(.+?)\s*Дані про взяття на облік',
    }

    tov_regex_dict = {
        'company_name': r'Повна назва: ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ\s\s*(.+?)\s*(Код:|Організаційно-правова форма:)',
        'edrpou': r'Код:\s*(.+?)\s*Реєстраційний номер:',
        'address': r'Адреса:\s*(.+?)\s*Статус:',
        'director_name': r'Керівник:\s*(.+?)\s*(Відомості про органи управління:|Засновник:|Представник:)',
        'phone': r'Контактна інформація(?:\s*Електронна пошта:.*?Телефон:| Телефон:.*?)\s*(.+?)\s*Дані про взяття на облік',
        'email': r'Контактна інформація\s*Електронна пошта:\s*(.+?)\s*Телефон:\s*(.+?)\s*Дані про взяття на облік',
    }

    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def text_extraction(self):
        pdf_reader = PyPDF2.PdfReader(self.pdf_file)

        extracted_text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text

        extracted_text = extracted_text.replace('\n', ' ')
        extracted_text = re.sub(r'[‘’“”"«»]', '', extracted_text)

        return extracted_text

    def is_fop(self) -> bool:
        extracted_text = self.text_extraction()

        has_fop = bool(re.search(r'\bФОП\b', extracted_text))
        has_tov = bool(re.search(r'\bТОВ\b', extracted_text))
        if has_fop:
            return True
        if has_tov:
            return False

    def extract_data(self) -> dict:
        extracted_text = self.text_extraction()

        is_fop = self.is_fop()

        if is_fop:
            regex_dict = self.fop_regex_dict
        else:
            regex_dict = self.tov_regex_dict

        extracted_data = {}
        for key, regex in regex_dict.items():
            match = re.search(regex, extracted_text, re.DOTALL)
            if match:
                extracted_data[key] = match.group(1).strip()
            else:
                extracted_data[key] = None
        return extracted_data

    @staticmethod
    def address_handler(text: str) -> str:
        replacement_patterns = [
            (r"(місто|м\.)", "м."),
            (r"(вулиця|вул\.|в\.)", "вулиця"),
            (r"(район|р-н|р\.)", "район"),
            (r"(область|обл\.)", "область"),
            (r"(смт)", "селище міського типу"),
            (r"(будинок|буд\.)", "будинок"),
            (r"(квартира|кв\.)", "квартира")
        ]

        text_without_word_ukraina = re.sub(r'\bУкраїна,\s*', '', text)
        text_without_duplicate_index = re.sub(r'\s+', ' ', text_without_word_ukraina)

        replaced_text = text_without_duplicate_index.title()

        for pattern, replacement in replacement_patterns:
            replaced_text = re.sub(
                fr"\b{pattern}\b",
                replacement,
                replaced_text,
                flags=re.IGNORECASE
            )

        return replaced_text

