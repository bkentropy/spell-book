from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.spells import search_spells

router = APIRouter()

@router.get("/search", response_class=HTMLResponse)
async def search_page(request: Request, q: str = ""):
    # Use the search service to get results
    results = search_spells(q)
    
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
