from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.models.schemas import ChatSessionSchema
from backend.models.database import get_db
from backend.services.history_service import history_service
import logging

router = APIRouter(prefix="/history", tags=["History"])
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[ChatSessionSchema])
async def get_history(limit: int = 10, db: Session = Depends(get_db)):
    """Retrieves recent chat sessions for the memory timeline."""
    try:
        sessions = history_service.get_all_sessions(db, limit)
        return sessions
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        return []

@router.get("/{session_id}", response_model=ChatSessionSchema)
async def get_session_details(session_id: str, db: Session = Depends(get_db)):
    """Retrieves a specific chat session with all its messages."""
    session = history_service.get_session(db, session_id)
    return session
