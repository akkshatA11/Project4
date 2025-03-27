from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from authlib.integrations.starlette_client import OAuth
from sqlalchemy import null
from starlette.middleware.sessions import SessionMiddleware
from database import auth_database, users
from pydantic import BaseModel
from typing import Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# OAuth configuration remains the same
oauth = OAuth()
oauth.register(
    "google",
    client_id="your_google_client_id",
    client_secret="your_google_client_secret",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    "facebook",
    client_id="your_facebook_client_id",
    client_secret="your_facebook_client_secret",
    authorize_url="https://www.facebook.com/v12.0/dialog/oauth",
    access_token_url="https://graph.facebook.com/v12.0/oauth/access_token",
    client_kwargs={"scope": "email public_profile"},
)

class UserSignup(BaseModel):
    username: str
    email: str
    password: str
    auth_provider: Optional[str] = None

@router.post("/signup")
async def signup(user_data: UserSignup):
    # Check if user exists first
    existing_email = await auth_database.fetch_one(
        users.select().where(users.c.email == user_data.email)
    )
    existing_username = await auth_database.fetch_one(
        users.select().where(users.c.username == user_data.username)
    )
    
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Store user (with plain text password in this example)
    await auth_database.execute(
        users.insert().values(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,  # Plain text storage
            auth_provider=user_data.auth_provider
        )
    )
    return {"message": "User created successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Find user by username
    user = await auth_database.fetch_one(
        users.select().where(users.c.username == form_data.username)
    )
    
    # 2. Verify user exists and password matches (plain text comparison)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Username not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if user["password"] != form_data.password:  # Plain text comparison
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # 3. Successful login
    return {
        "message": "Login successful",
        "user": {
            "username": user["username"],
            "email": user["email"]
        }
    }

# OAuth endpoints remain unchanged
@router.get("/login/google")
async def login_google():
    return await oauth.google.authorize_redirect("http://localhost:8000/auth/google")

@router.get("/auth/google")
async def auth_google(request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    return {"email": user_info["email"], "name": user_info["name"]}

@router.get("/login/facebook")
async def login_facebook():
    return await oauth.facebook.authorize_redirect("http://localhost:8000/auth/facebook")

@router.get("/auth/facebook")
async def auth_facebook(request):
    token = await oauth.facebook.authorize_access_token(request)
    resp = await oauth.facebook.get("https://graph.facebook.com/me?fields=id,name,email", token=token)
    user_info = resp.json()
    return {"email": user_info.get("email"), "name": user_info["name"]}