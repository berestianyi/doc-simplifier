import logging

from src.documents.services.dto import BusinessEntityDTO
from src.documents.services.formatters import BusinessEntityDataFormatter
from src.documents.services.text_extraction import OpenDataBotTextExtraction


class DocumentService:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.logger = logging.getLogger(__name__)
        self.extractor = OpenDataBotTextExtraction(pdf_file)
        self.formatter = BusinessEntityDataFormatter()

    def extract_data(self) -> BusinessEntityDTO:
        try:
            extracted_data = self.extractor.extract()
            formatted_data = self.formatter.format_entity_data(extracted_data)
            return formatted_data
        except Exception as e:
            self.logger.error(f"Error processing document: {e}")
            raise

    @staticmethod
    def is_fop(text) -> bool:
        if len(text) == 8:
            return False
        return True
