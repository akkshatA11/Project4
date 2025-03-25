from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from .database import auth_database, users  # Use auth database

router = APIRouter()

# Session Middleware should be added in main.py, not here.
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


@router.post("/signup")
async def signup(username: str, email: str, password: str):
    query = users.insert().values(username=username, email=email, password=password)
    await auth_database.execute(query)  # Use auth database
    return {"message": "User created successfully"}


@router.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    query = users.select().where(users.c.username == form_data.username)
    user = await auth_database.fetch_one(query)  # Use auth database

    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Store user session
    request.session["user"] = {"username": user["username"], "email": user["email"]}

    return {"message": "Login successful"}


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()  # Remove user session
    return {"message": "Logged out successfully"}



@router.get("/me")
async def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


@router.get("/login/google")
async def login_google():
    return await oauth.google.authorize_redirect("http://localhost:8000/auth/google")


@router.get("/auth/google")
async def auth_google(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)

    query = users.select().where(users.c.email == user_info["email"])
    existing_user = await auth_database.fetch_one(query)

    if not existing_user:
        # Insert new OAuth user
        query = users.insert().values(
            username=user_info["name"],
            email=user_info["email"],
            password=None,  
            auth_provider="google",
            provider_id=user_info["sub"]
        )
        await auth_database.execute(query)

    # Store user session
    request.session["user"] = {"email": user_info["email"], "name": user_info["name"]}

    return {"email": user_info["email"], "name": user_info["name"]}


@router.get("/login/facebook")
async def login_facebook():
    return await oauth.facebook.authorize_redirect("http://localhost:8000/auth/facebook")


@router.get("/auth/facebook")
async def auth_facebook(request: Request):
    token = await oauth.facebook.authorize_access_token(request)
    resp = await oauth.facebook.get("https://graph.facebook.com/me?fields=id,name,email", token=token)
    user_info = resp.json()

     # Check if user exists in the database
    query = users.select().where(users.c.email == user_info.get("email"))
    existing_user = await auth_database.fetch_one(query)

    if not existing_user:
        # Insert new OAuth user
        query = users.insert().values(
            username=user_info["name"],
            email=user_info.get("email"),
            password=None, 
            auth_provider="facebook",
            provider_id=user_info["id"]
        )
        await auth_database.execute(query)

    # Store user session
    request.session["user"] = {"email": user_info.get("email"), "name": user_info["name"]}

    return {"email": user_info.get("email"), "name": user_info["name"]}
