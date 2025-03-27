from fastapi import FastAPI, WebSocket
from database import shortener_metadata, shortener_engine, auth_metadata, auth_engine
from routes import router as url_router
from auth import router as auth_router  

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (adjust origins as needed)
origins = [
    "http://localhost:3000",  # React dev server
    "http://your-production-domain.com"  # Add production domain here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")
        
# Create database tables for both databases
shortener_metadata.create_all(bind=shortener_engine)
auth_metadata.create_all(bind=auth_engine)

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Include URL shortener routes
app.include_router(url_router, prefix="/url", tags=["URL Shortener"])