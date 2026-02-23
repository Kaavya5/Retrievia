import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(filepath: str) -> str:
    """Extracts text from a PDF file using PyMuPDF."""
    text = ""
    try:
        doc = fitz.open(filepath)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text() + "\n"
    except Exception as e:
        logger.error(f"Failed to read PDF {filepath}: {e}")
        raise e
    return text

def extract_text_from_txt(filepath: str) -> str:
    """Extracts text from a standard text or markdown file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read TXT/MD {filepath}: {e}")
        raise e

def parse_document(filepath: str, filename: str) -> str:
    """Delegates parsing based on file extension."""
    if filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(filepath)
    elif filename.lower().endswith(".txt") or filename.lower().endswith(".md"):
        return extract_text_from_txt(filepath)
    else:
        raise ValueError("Unsupported file format. Please upload PDF, TXT, or MD.")
