from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import auth, spells
from app.database import users
from app.security import hash_password

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.state.templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(spells.router)

@app.on_event("startup")
async def startup_db_client():
    # Create sample user if it doesn't exist
    if not users.find_one({"username": "brian"}):
        user_data = {
            "username": "brian",
            "hashed_password": hash_password("kustra"),
            "email": "brian@example.com",
            "is_active": True
        }
        users.insert_one(user_data)

@app.get("/")
async def root():
    return {"message": "Go to /login"}
