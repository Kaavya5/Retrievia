import logging
from typing import List

logger = logging.getLogger(__name__)

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Splits text into chunks of `chunk_size` characters with `overlap` characters.
    This is a simple character-based chunking which works reasonably well.
    For more advanced semantic logic, LangChain's RecursiveCharacterTextSplitter is ideal,
    but we keep dependencies lean here.
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        
        # Advance by the size of the chunk minus the overlap
        start += (chunk_size - overlap)
        
        # Prevent infinite loops if chunk_size is smaller than overlap
        if chunk_size <= overlap:
            logger.warning("Chunk size is <= overlap. Setting advance to 1 to prevent infinite loop.")
            start += 1
            
    return chunks
