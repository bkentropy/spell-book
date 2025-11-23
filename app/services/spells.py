from typing import List, Dict, Any
from app.database import spells

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
    
    # Create text search pipeline
    pipeline = [
        {
            "$search": {
                "index": "default",
                "text": {
                    "query": q,
                    "path": {
                        "wildcard": "*"
                    }
                }
            }
        },
        {"$match": {"resource_type": "spells"}},
        {"$limit": 20}
    ]
    
    # Execute the aggregation pipeline
    return list(spells.aggregate(pipeline))
