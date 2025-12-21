from langchain_chroma import Chroma
from .huggingface import huggingface_embedding
import uuid

def embedding(chunks):
    upload_id = str(uuid.uuid4())
    persist_dir = f"chroma_db/{upload_id}"
    embedding_model = huggingface_embedding()
    vector_store = Chroma(
        embedding_function=embedding_model,
        persist_directory=persist_dir,
        collection_name='pdf_collection'
    )
    vector_store.add_documents(documents=chunks)
    return vector_store

