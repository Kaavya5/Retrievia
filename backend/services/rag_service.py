import os
import uuid
import logging
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict

logger = logging.getLogger(__name__)

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./vector_store")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

class RAGService:
    def __init__(self):
        # Initialize the local persistent vector DB
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        
        # Determine the embedding dimension (using default for all-minilm)
        self.collection_name = "second_brain_docs"
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name)
        
        # Initialize embedding model (runs locally)
        logger.info(f"Loading embedding model {EMBEDDING_MODEL_NAME}...")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        logger.info("Embedding model loaded.")

    def add_document_chunks(self, document_id: str, document_name: str, chunks: List[str]):
        """Embeds text chunks and stores them in ChromaDB."""
        if not chunks:
            return

        logger.info(f"Embedding {len(chunks)} chunks for document {document_id}")
        # Generate embeddings
        embeddings = self.embedding_model.encode(chunks)
        
        # Generate IDs and metadata
        ids = [f"{document_id}_{i}" for i in range(len(chunks))]
        metadatas = [{"document_id": document_id, "document_name": document_name} for _ in range(len(chunks))]
        
        # Add to vector store
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Added document {document_id} chunks to Chroma DB.")

    def query_similarity(self, query: str, top_k: int = 4, document_id: str = None) -> List[Dict]:
        """Queries the vector database for the most similar chunks."""
        # Embed query
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search collection
        kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": top_k
        }
        if document_id:
            kwargs["where"] = {"document_id": document_id}
            
        results = self.collection.query(**kwargs)
        
        # Format results
        final_results = []
        if results and "documents" in results and "distances" in results:
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            distances = results['distances'][0]
            
            for i in range(len(documents)):
                final_results.append({
                    "text": documents[i],
                    "document_id": metadatas[i].get("document_id"),
                    "document_name": metadatas[i].get("document_name"),
                    "score": distances[i] # Distances depending on metric used (L2 by default in Chroma)
                })
        
        return final_results

# Create a singleton instance to be used by the app
rag_service = RAGService()
