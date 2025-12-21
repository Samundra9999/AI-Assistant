import fitz
import io


def pdf_to_images(pdf_bytes):
    pdf_stream = io.BytesIO(pdf_bytes)
    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    images = []

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        path = f"page_{i+1}.png"
        pix.save(path) 
        images.append(path)

    return images
