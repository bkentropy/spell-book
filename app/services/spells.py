import re
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
    
    # Create a case-insensitive regex pattern
    pattern = {"$regex": q, "$options": "i"}
    
    # Find matching documents using $or with regex
    matching_docs = list(spells.find({
        "resource_type": "spells",
        "$or": [
            {"name": pattern},
            {"desc": pattern}
        ]
    }).limit(50))  # Get more than needed to sort in memory
    
    # Calculate relevance score in Python
    for doc in matching_docs:
        doc['relevance'] = 0
        if 'name' in doc and doc['name'] and isinstance(doc['name'], str) and re.search(q, doc['name'], re.IGNORECASE):
            doc['relevance'] += 2
        if 'desc' in doc and doc['desc'] and isinstance(doc['desc'], str) and re.search(q, doc['desc'], re.IGNORECASE):
            doc['relevance'] += 1
    
    # Sort by relevance (desc) and then by name (asc)
    return sorted(
        matching_docs,
        key=lambda x: (-x.get('relevance', 0), x.get('name', '').lower())
    )[:20]  # Take top 20
