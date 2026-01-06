from sentence_transformers import SentenceTransformer

# Initialize the model once (high-performance semantic model)
model = SentenceTransformer('all-mpnet-base-v2')

def get_embedding(text: str) -> list:
    """Generate embeddings using sentence-transformers (local, no API calls)."""
    embedding = model.encode(text)
    return embedding.tolist()
