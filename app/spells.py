from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.database import spells

router = APIRouter()

@router.get("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    return request.app.state.templates.TemplateResponse("search.html", {"request": request})

@router.get("/search-spells", response_class=HTMLResponse)
async def search_spells(request: Request, q: str = ""):
    query = {"name": {"$regex": q, "$options": "i"}} if q else {}
    results = list(spells.find(query).limit(20))

    return request.app.state.templates.TemplateResponse(
        "spell_card.html",
        {"request": request, "spells": results}
    )
