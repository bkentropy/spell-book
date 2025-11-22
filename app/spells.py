from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.database import spells

router = APIRouter()

@router.get("/search", response_class=HTMLResponse)
async def search_page(request: Request, q: str = ""):
    # Base query always includes resource_type: "spells"
    query = {"resource_type": "spells"}
    
    # Add regex search for name and desc if query is provided
    if q:
        regex = {"$regex": q, "$options": "i"}
        query["$or"] = [
            {"name": regex},
            {"desc": regex}
        ]
    
    # Get results with limit
    results = list(spells.find(query).limit(20))
    
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
