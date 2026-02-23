import os
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.models.schemas import DocumentResponse
from backend.utils.document_parser import parse_document
from backend.utils.text_chunker import chunk_text
from backend.services.rag_service import rag_service

router = APIRouter(prefix="/documents", tags=["Documents"])
logger = logging.getLogger(__name__)

DATA_DIR = os.getenv("DATA_DIR", "./data")
os.makedirs(DATA_DIR, exist_ok=True)

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """Uploads a document, parses it, chunks it, and adds to ChromaDB."""
    try:
        # Save file locally
        document_id = str(uuid.uuid4())
        filepath = os.path.join(DATA_DIR, f"{document_id}_{file.filename}")
        
        with open(filepath, "wb") as f:
            f.write(await file.read())
            
        # Parse document
        text = parse_document(filepath, file.filename)
        if not text.strip():
            raise HTTPException(status_code=400, detail="No readable text found in document.")
            
        # Chunk text
        chunks = chunk_text(text)
        
        # Embed and store
        rag_service.add_document_chunks(document_id, file.filename, chunks)
        
        return DocumentResponse(
            document_id=document_id,
            filename=file.filename,
            message=f"Successfully ingested document '{file.filename}' into {len(chunks)} chunks."
        )
        
    except Exception as e:
        logger.error(f"Error handling document upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))
