from typing import List, Dict, Any
from app.database import spells
from app.services.embedding import EmbeddingClient

def search_spells(q: str = "") -> List[Dict[str, Any]]:
    """
    Search for spells by name or description with relevance scoring.
    
    Args:
        q: Search query string
        
    Returns:
        List of spell documents with relevance scores, sorted by relevance and name
    """
    # Base query always includes resource_type: "spells"
    query = {"resource_type": "spells"}
    
    # If no query, return first 20 spells sorted by name
    if not q:
        return list(spells.find(query).sort("name", 1).limit(20))
    
    # Get text search results
    text_results = list(spells.aggregate([
        {
            "$search": {
                "index": "default",
                "text": {
                    "query": q,
                    "path": {"wildcard": "*"},
                    "score": {"boost": {"value": 2.0}}  # Higher weight for text matches
                }
            }
        },
        {"$match": {"resource_type": "spells"}},
        {"$limit": 40}  # Get more results to combine with vector search
    ]))
    
    # Get vector search results if we have an embedding for the query
    try:
        # Get embedding for the query
        embedding_client = EmbeddingClient()
        query_embedding = embedding_client.get_embedding(q).get("embeddings")[0]
        
        vector_results = list(spells.aggregate([
            {
                "$vectorSearch": {
                    "index": "spell_desc_index",
                    "path": "desc_embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 50,
                    "limit": 40,
                    "score": {"score": {"$meta": "vectorSearchScore"}}
                }
            },
            {"$match": {"resource_type": "spells"}}
        ]))
        
        # Combine and rank results
        combined = {}
        
        # Add text search results with higher weight
        for doc in text_results:
            doc_id = str(doc['_id'])
            combined[doc_id] = {
                'doc': doc,
                'score': doc.get('score', 0) * 2.0  # Higher weight for text matches
            }
        
        # Add or update with vector search results
        for doc in vector_results:
            doc_id = str(doc['_id'])
            vector_score = doc.get('score', 0)
            if doc_id in combined:
                combined[doc_id]['score'] += vector_score
            else:
                combined[doc_id] = {
                    'doc': doc,
                    'score': vector_score
                }
        
        # Sort by combined score and get top 20
        sorted_results = sorted(
            combined.values(),
            key=lambda x: -x['score']
        )
        
        # Return just the documents, not the scores
        return [r['doc'] for r in sorted_results[:20]]
        
    except Exception as e:
        print(f"Error in vector search, falling back to text search: {str(e)}")
        return text_results[:20]  # Fallback to just text search if vector search fails
