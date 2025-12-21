from .pdf_ocr_preprocessing import pdf_to_images
from .ocr import paddle_ocr
from .pdf_text import text_handler


def pdf_handler(source):
    try:
        text = text_handler(source)
        text = text.replace("CamScanner", "")
        if len(text.split()) < 500:
            images = pdf_to_images(source)
            text = paddle_ocr(images=images)
        return text
    except FileNotFoundError:
        return "File Not Found"
    