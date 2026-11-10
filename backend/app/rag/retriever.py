"""RAG Document Chunking, Embedding & Retrieval Module.
Handles:
- Text extraction from Brand Guidelines, Product Info, & Campaign Reports
- Recursive text chunking with overlap
- Lightweight semantic / vector representation and similarity search
- Brand-isolated context retrieval for Agents
"""

import math
import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models import Document, DocumentChunk, Brand

CHUNK_SIZE = 500
CHUNK_OVERLAP = 80

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Splits a document text into overlapping chunks."""
    clean_text = re.sub(r'\s+', ' ', text).strip()
    if not clean_text:
        return []

    chunks = []
    start = 0
    while start < len(clean_text):
        end = start + chunk_size
        chunk = clean_text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def compute_simple_embedding(text: str) -> Dict[str, float]:
    """
    Computes a normalized term-frequency vector representation.
    Ensures lightweight semantic similarity retrieval even without GPU or external models,
    while being fully compatible with pgvector/JSON storage.
    """
    words = re.findall(r'[a-zA-Z0-9_]{3,}', text.lower())
    if not words:
        return {}

    tf = {}
    for w in words:
        tf[w] = tf.get(w, 0) + 1

    # Normalize vector length
    norm = math.sqrt(sum(v * v for v in tf.values())) or 1.0
    return {k: round(v / norm, 4) for k, v in tf.items()}

def cosine_similarity(v1: Dict[str, float], v2: Dict[str, float]) -> float:
    """Computes cosine similarity between two term-frequency sparse vectors."""
    if not v1 or not v2:
        return 0.0
    common_keys = set(v1.keys()) & set(v2.keys())
    return sum(v1[k] * v2[k] for k in common_keys)

class RAGRetriever:
    def process_and_store_document(
        self,
        document: Document,
        text_content: str,
        db: Session
    ) -> int:
        """Chunks document, computes embeddings, and stores document_chunks."""
        chunks = chunk_text(text_content)
        stored_count = 0

        for idx, chunk in enumerate(chunks):
            embedding = compute_simple_embedding(chunk)
            chunk_obj = DocumentChunk(
                document_id=document.id,
                brand_id=document.brand_id,
                chunk_index=idx,
                chunk_text=chunk,
                embedding=embedding
            )
            db.add(chunk_obj)
            stored_count += 1

        document.processing_status = "completed"
        db.commit()
        return stored_count

    def retrieve_relevant_chunks(
        self,
        brand_id: int,
        query: str,
        db: Session,
        top_k: int = 4
    ) -> List[Dict[str, Any]]:
        """Retrieves top-k relevant chunks for this brand matching the query."""
        chunks = db.query(DocumentChunk).filter(DocumentChunk.brand_id == brand_id).all()
        if not chunks:
            return []

        query_vec = compute_simple_embedding(query)
        scored_chunks = []

        for c in chunks:
            sim = cosine_similarity(query_vec, c.embedding or {})
            scored_chunks.append({
                "chunk_id": c.id,
                "document_id": c.document_id,
                "text": c.chunk_text,
                "similarity": round(sim, 4)
            })

        # Sort by similarity
        scored_chunks.sort(key=lambda x: x["similarity"], reverse=True)
        return scored_chunks[:top_k]

rag_retriever = RAGRetriever()

