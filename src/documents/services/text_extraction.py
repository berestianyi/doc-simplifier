import PyPDF2
import logging
import re

from documents.services.dto import BusinessEntityDTO


class OpenDataBotTextExtraction:
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
        self.logger = logging.getLogger(__name__)

    def _text_extraction(self):
        try:
            pdf_reader = PyPDF2.PdfReader(self.pdf_file)

            extracted_text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text

            extracted_text = extracted_text.replace('\n', ' ')
            extracted_text = re.sub(r'[‘’“”"«»]', '', extracted_text)

            return extracted_text

        except Exception as e:
            self.logger.error(f"Error reading PDF: {e}")
            raise

    def _is_fop(self, text) -> bool:

        has_fop = bool(re.search(r'\bФОП\b', text))
        has_tov = bool(re.search(r'\bТОВ\b', text))
        if has_fop:
            return True
        if has_tov:
            return False

    def _validate_edrpou(self, edrpou: str) -> bool:
        return len(edrpou) in (8, 10) and edrpou.isdigit()

    def extract(self) -> BusinessEntityDTO:
        try:
            text = self._text_extraction()
            is_fop = self._is_fop(text)
            regex_dict = self.fop_regex_dict if is_fop else self.tov_regex_dict
            entity_type = "ФОП" if is_fop else "ТОВ"

            data: BusinessEntityDTO = {
                'business_entity': entity_type,
                'edrpou': '',
                'company_name': '',
                'director_name': '',
                'address': '',
                'phone': '',
                'email': ''
            }

            for key, pattern in regex_dict.items():
                match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    if key == 'edrpou' and not self._validate_edrpou(value):
                        continue
                    data[key] = value

            return data
        except Exception as e:
            self.logger.error(f"Extraction error: {e}")
            raise
