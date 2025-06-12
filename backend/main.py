from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
import shutil
from .schemas import Query
from .database import store_chunks, get_relevant_chunks, get_all_documents
from .text_extraction import extract_chunks_from_file
from .llm import identify_themes_and_summarize

app = FastAPI()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        chunks = extract_chunks_from_file(file_path)
        if not chunks:
            raise ValueError("Could not extract any text chunks from the file. It may be empty or in an unsupported format.")

        store_chunks(chunks)
        
        return JSONResponse(content={"filename": file.filename, "chunks_stored": len(chunks)}, status_code=200)
    except Exception as e:
        print(f"An error occurred during file upload: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {e}")

@app.post("/query/")
async def query_documents(query: Query):
    try:
        # Pass the document filter from the query model to the database function
        relevant_chunks = get_relevant_chunks(query.text, documents=query.documents)
        if not relevant_chunks:
            return {"summary": {"summary": "No relevant information found in the selected documents."}, "relevant_docs": []}

        summary = identify_themes_and_summarize(query.text, relevant_chunks)
        
        # The relevant_chunks already contain the citation data
        return {"summary": summary, "relevant_docs": relevant_chunks}
    except Exception as e:
        print(f"An error occurred during query: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during query: {e}")

@app.get("/documents/")
async def list_documents():
    """Endpoint to get a list of all uploaded documents."""
    try:
        documents = get_all_documents()
        return JSONResponse(content={"documents": documents}, status_code=200)
    except Exception as e:
        print(f"An error occurred while listing documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve document list.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)