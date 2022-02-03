import re
import pytesseract
from pdf2image import convert_from_bytes


def ocr(bts: bytes, dpi=300) -> str:
    pages = convert_from_bytes(bts, dpi=dpi)
    text = " ".join(map(pytesseract.image_to_string, pages))
    clean_text = re.sub(r"\s+", " ", text)
    return clean_text
