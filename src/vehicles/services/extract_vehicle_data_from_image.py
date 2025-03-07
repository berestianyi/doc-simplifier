import cv2
import pytesseract
import re


class ExtractVehicleDataFromImage:

    def _preprocess_image(self, image_path):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return thresh

    def _extract_text(self, image_path):
        processed_img = self._preprocess_image(image_path)
        text = pytesseract.image_to_string(processed_img, lang='rus+eng')
        return text

    def _find_car_number(self, text) -> str:
        pattern = r'\b[АВЕКМНОРСТУХA-Z]\d{3}[АВЕКМНОРСТУХA-Z]{2}\d{2,3}\b'
        return re.findall(pattern, text, re.IGNORECASE)[0] if re.findall(pattern, text) else ''

    def _find_model(self, text) -> str:
        pass

    def _find_brand(self, text) -> str:
        brands = [
            "MERCEDES-BENZ",
            "VOLKSWAGEN",
            "MAN",
            "SCANIA",
            "VOLVO",
            "DAF",
            "RENAULT",
            "IVECO",
            "KAMAZ",
            "MAZ",
            "URAL",
            "FOTON",
            "HOWO",
            "FAW",
            "SHACMAN",
            "HINO",
            "ISUZU",
            "TATA",
            "ASHOK LEYLAND",
            "HYUNDAI",
            "KENWORTH",
            "PETERBILT",
            "FREIGHTLINER",
            "MACK",
            "INTERNATIONAL",
            "WESTERN STAR"
        ]

        return next((b for b in brands if b.lower() in text.lower()), '')

    def _find_vin(self, text) -> str:
        vin_pattern = r'\b[(A-HJ-NPR-Z0-9)]{17}\b'
        matches = re.findall(vin_pattern, text, re.IGNORECASE)
        return matches[0] if matches else ''

    def execute(self, image_path) -> dict:
        text = self._extract_text(image_path)

        return {
            'car_number': self._find_car_number(text),
            'brand': self._find_brand(text),
            'vin': self._find_vin(text)
        }
