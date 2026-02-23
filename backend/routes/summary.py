import os
import glob
import logging
from fastapi import APIRouter, HTTPException
from backend.models.schemas import SummaryRequest, SummaryResponse
from backend.services.llm_service import llm_service
from backend.utils.document_parser import parse_document

router = APIRouter(prefix="/summary", tags=["Summary"])
logger = logging.getLogger(__name__)

DATA_DIR = os.getenv("DATA_DIR", "./data")

@router.post("/", response_model=SummaryResponse)
async def summarize_document(request: SummaryRequest):
    """Summarizes a previously uploaded document."""
    document_id = request.document_id
    
    # We need to find the file locally since we don't store full original text in ChromaDB directly.
    # Searching for file matching document_id in DATA_DIR
    search_pattern = os.path.join(DATA_DIR, f"{document_id}_*")
    matches = glob.glob(search_pattern)
    
    if not matches:
        raise HTTPException(status_code=404, detail="Document original file not found on server.")
        
    filepath = matches[0]
    filename = os.path.basename(filepath).replace(f"{document_id}_", "")

    try:
        # Read text
        text = parse_document(filepath, filename)
        
        if not text.strip():
             raise HTTPException(status_code=400, detail="Document contains no text to summarize.")
             
        # Generate summary
        summary = llm_service.summarize_document(text)
        
        return SummaryResponse(
            document_id=document_id,
            summary=summary
        )
    except Exception as e:
        logger.error(f"Error summarising document {document_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
