import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models.database import engine, Base

# Import routers
from backend.routes import document, chat, summary, history

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize database schemas
logger.info("Initializing database schemas...")
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Second Brain API",
    description="API for personal knowledge assistant with RAG.",
    version="1.0.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(document.router)
app.include_router(chat.router)
app.include_router(summary.router)
app.include_router(history.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Second Brain API"}
