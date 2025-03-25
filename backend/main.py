from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from .database import shortener_metadata, shortener_engine, auth_metadata, auth_engine
from .routes import router as url_router
from .auth import router as auth_router  
from .qrcode import router as qr_router 

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Create database tables for both databases
shortener_metadata.create_all(bind=shortener_engine)
auth_metadata.create_all(bind=auth_engine)

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Include URL shortener routes
app.include_router(url_router, prefix="/url", tags=["URL Shortener"])

# Include QR Code generator routes
app.include_router(qr_router, prefix="/qr", tags=["QR Code Generator"])
