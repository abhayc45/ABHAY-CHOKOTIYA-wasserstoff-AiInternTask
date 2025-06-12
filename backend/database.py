from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, PointStruct, ScrollRequest, Filter, FieldCondition, MatchValue
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Qdrant client
# For production, you might want to use a persistent Qdrant instance
qdrant_client = QdrantClient(":memory:")

COLLECTION_NAME = "chatbot_documents_v2"

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_embedding(text: str, task_type: str = "retrieval_document"):
    """Generates an embedding for the given text using the Gemini model."""
    try:
        # Note: The task_type for querying should be "retrieval_query"
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type=task_type
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Handle cases where the API key might be invalid or other issues
        raise ValueError("Failed to generate embedding. Check your API key and network connection.") from e

def setup_database():
    """Creates the Qdrant collection if it doesn't exist."""
    try:
        qdrant_client.get_collection(collection_name=COLLECTION_NAME)
    except Exception:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

def store_chunks(chunks: List[Dict[str, Any]]):
    """Stores a list of text chunks in the Qdrant database."""
    if not chunks:
        return

    points_to_upsert = []
    for chunk_data in chunks:
        embedding = get_embedding(chunk_data["content"])
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "content": chunk_data["content"],
                **chunk_data["metadata"] # Unpack metadata directly into payload
            }
        )
        points_to_upsert.append(point)

    if points_to_upsert:
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points_to_upsert,
            wait=True
        )

def get_relevant_chunks(query_text: str, limit: int = 5, documents: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Retrieves the most relevant document chunks for a given query, with an optional document filter."""
    query_embedding = get_embedding(query_text, task_type="retrieval_query")
    
    search_filter = None
    if documents:
        search_filter = Filter(
            must=[
                FieldCondition(
                    key="source",
                    match=MatchValue(value=doc_name)
                ) for doc_name in documents
            ]
        )

    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        query_filter=search_filter,
        limit=limit,
        with_payload=True # Ensure payload is returned
    )
    # The payload is now directly the hit's payload
    return [hit.payload for hit in search_result]

def get_all_documents() -> List[str]:
    """Retrieves a list of all unique document sources from the database."""
    # This is a simplified approach for in-memory/small datasets.
    # For large datasets, a more efficient method would be needed.
    all_points, _ = qdrant_client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=None,
        limit=10000, # Adjust limit as needed
        with_payload=["source"]
    )
    
    unique_sources = set(point.payload['source'] for point in all_points if 'source' in point.payload)
    return sorted(list(unique_sources))

# Initialize the database when the module is loaded
setup_database()