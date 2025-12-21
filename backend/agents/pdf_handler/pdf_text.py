from langchain_community.document_loaders import PyPDFLoader
import tempfile
import io

def text_handler(pdf_bytes):
    source = io.BytesIO(pdf_bytes)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(source.read())
        tmp_path = tmp_file.name
    loader = PyPDFLoader(file_path=tmp_path)
    text = []
    for i in loader.load():
        text.append(i.page_content)
    final_text = " ".join(text)
    return final_text
