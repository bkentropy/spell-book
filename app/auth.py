from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import RedirectResponse
from app.database import users
from app.security import verify_password
from itsdangerous import URLSafeSerializer

router = APIRouter()
serializer = URLSafeSerializer("SECRET_KEY", salt="auth")



def get_current_user(request: Request):
    session = request.cookies.get("session")
    if not session:
        return None
    try:
        data = serializer.loads(session)
        return users.find_one({"username": data["username"]})
    except Exception:
        return None

@router.get("/login")
async def login_page(request: Request):
    return request.app.state.templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_user(response: Response, username: str = Form(...), password: str = Form(...)):
    user = users.find_one({"username": username})
    if not user or not verify_password(password, user["hashed_password"]):
        return RedirectResponse("/login?error=1", status_code=303)

    session = serializer.dumps({"username": username})
    response = RedirectResponse("/search", status_code=303)
    response.set_cookie("session", session, httponly=True, samesite="lax")
    return response
