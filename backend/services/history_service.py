from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models.orm_models import ChatSession, ChatMessage
from backend.models.schemas import ChatSessionSchema, ChatMessageSchema
import logging

logger = logging.getLogger(__name__)

class HistoryService:
    @staticmethod
    def create_session(db: Session, title: str = "New Chat") -> ChatSession:
        db_session = ChatSession(title=title)
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    @staticmethod
    def get_session(db: Session, session_id: str) -> Optional[ChatSession]:
        return db.query(ChatSession).filter(ChatSession.id == session_id).first()

    @staticmethod
    def get_all_sessions(db: Session, limit: int = 10) -> List[ChatSession]:
        return db.query(ChatSession).order_by(ChatSession.created_at.desc()).limit(limit).all()

    @staticmethod
    def add_message(db: Session, session_id: str, role: str, content: str) -> ChatMessage:
        msg = ChatMessage(session_id=session_id, role=role, content=content)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg
    
    @staticmethod
    def get_session_history(db: Session, session_id: str) -> List[ChatMessage]:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            return session.messages
        return []

history_service = HistoryService()
