from paddleocr import PaddleOCR

def paddle_ocr(images):
    Ocr = PaddleOCR(lang="en")
    results = Ocr.predict(images)
    all_text = []
    for result in results:
        list_text = result["rec_texts"]
        text = " ".join(list_text)
        all_text.append(text)
    return "\n".join(all_text)

