from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.database import spells

router = APIRouter()

@router.get("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    return request.app.state.templates.TemplateResponse("search.html", {"request": request})

@router.get("/search-spells", response_class=HTMLResponse)
async def search_spells(request: Request, q: str = ""):
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

    return request.app.state.templates.TemplateResponse(
        "spell_card.html",
        {"request": request, "spells": results}
    )
