import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.schemas import ChatRequest, ChatResponse, SourceChunk
from backend.models.database import get_db
from backend.services.rag_service import rag_service
from backend.services.llm_service import llm_service
from backend.services.history_service import history_service

router = APIRouter(prefix="/chat", tags=["Chat"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=ChatResponse)
async def complete_chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Handles chat queries against ingested documents."""
    query = request.query
    session_id = request.session_id
    
    # Handle session
    if not session_id:
        # Create a new session using the first few words of query as title
        title = query[:30] + "..." if len(query) > 30 else query
        session = history_service.create_session(db, title=title)
        session_id = session.id
    else:
        session = history_service.get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

    try:
        # 1. Retrieve similar chunks (if a document is specified)
        similar_chunks = []
        if request.document_id:
            similar_chunks = rag_service.query_similarity(query, top_k=4, document_id=request.document_id)
        
        # 2. Get history
        db_history = history_service.get_session_history(db, session_id)
        history_msgs = [{"role": msg.role, "content": msg.content} for msg in db_history]
        
        # 3. Generate response using LLM
        answer = llm_service.generate_chat_response(query, similar_chunks, history_msgs)
        
        # 4. Save to history
        history_service.add_message(db, session_id, role="user", content=query)
        history_service.add_message(db, session_id, role="assistant", content=answer)
        
        # 5. Format sources
        sources = [SourceChunk(
            text=chunk['text'], 
            document_id=chunk['document_id'],
            score=chunk['score']
        ) for chunk in similar_chunks]
        
        return ChatResponse(
            session_id=session_id,
            answer=answer,
            sources=sources
        )

    except Exception as e:
        logger.error(f"Error handling chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
