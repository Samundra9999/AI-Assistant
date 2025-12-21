from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import Optional
from PIL import Image
import io
import numpy as np
import logging

from .pdf_handler.main_pdf_handler import pdf_handler
from .pdf_handler.image_clean import image_content
from .clean_text.clean_text import clean_text
from .pdf_handler.ocr import paddle_ocr
from .chunking import chunker
from .embedding import embedding
from .retrieval import retreival_content

app = FastAPI(title="AI Research Backend")

app.state.vector_stores = {}         
app.state.image_questions = {}


@app.post("/process")
async def process(
    text: str = Form(...),
    pdf: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None)
    ):


    result = {
        "text_query": text,
        "pdf_text": None,
        "image_questions": None,
        "vector_store": None,
        "final_answer": None
    }


    if pdf:
        try:
            pdf_bytes = await pdf.read()
            extracted_text = pdf_handler(pdf_bytes)
            cleaned = clean_text(extracted_text)
            chunks = chunker(cleaned)
            vector_store = embedding(chunks)
            app.state.vector_store = vector_store
        except Exception as e:
            return JSONResponse({"error": f"PDF processing failed: {e}"}, 400)

 
    if image:
        try:
            img_bytes = await image.read()
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            img_np = np.array(img)  
            ocr_text = paddle_ocr([img_np])
            questions = image_content(ocr_text)
            app.state.image_questions = questions
        except Exception as e:
            return JSONResponse({"error": f"Image processing failed: {e}"}, 400)
        
    if hasattr(app.state, "vector_store"):
        vector_store = app.state.vector_store
    else:
        vector_store = None
    
    if hasattr(app.state, "image_questions"):
        image_questions_data = app.state.image_questions
    else:
        image_questions_data = None


    if isinstance(image_questions_data, list) and image_questions_data:
        query_to_use = image_questions_data
    else:
        query_to_use = result["text_query"]

    answers = retreival_content(
        vector_store=vector_store,
        image_content=image_questions_data,
        query=query_to_use
        )
    result["final_answer"] = answers
    return JSONResponse(result)

