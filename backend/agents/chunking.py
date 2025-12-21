from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def chunker(content):
    splitter = RecursiveCharacterTextSplitter(separators= "\n",chunk_size=500, chunk_overlap = 100)
    chunks = splitter.split_text(content)
    chunks = [Document(page_content=chunk) for chunk in chunks]
    return chunks

