import re
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.database import spells

router = APIRouter()

@router.get("/search", response_class=HTMLResponse)
async def search_page(request: Request, q: str = ""):
    # Base query always includes resource_type: "spells"
    query = {"resource_type": "spells"}
    
    # Add regex search with relevance scoring if query is provided
    if q:
        # Create a case-insensitive regex pattern
        pattern = {"$regex": q, "$options": "i"}
        
        # First, find matching documents using $or with regex
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
        results = sorted(
            matching_docs,
            key=lambda x: (-x.get('relevance', 0), x.get('name', '').lower())
        )[:20]  # Take top 20
    else:
        # If no search query, just get the first 20 spells
        results = list(spells.find(query).sort("name", 1).limit(20))
    
    # Check if this is an HTMX request
    is_htmx = request.headers.get("HX-Request") == "true"
    
    if is_htmx:
        # Return just the spell cards for HTMX requests
        return request.app.state.templates.TemplateResponse(
            "spell_card.html",
            {"request": request, "spells": results}
        )
    else:
        # Return the full page for regular requests
        return request.app.state.templates.TemplateResponse(
            "search.html",
            {"request": request, "spells": results}
        )
