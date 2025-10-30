from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, chat, export

app = FastAPI(
    title="Video Editor API",
    description="Chat-based video editing with subtitle overlay",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(export.router, prefix="/api", tags=["Export"])


@app.get("/")
async def root():
    return {
        "message": "Video Editor API",
        "status": "running",
        "endpoints": {
            "upload": "/api/upload",
            "chat": "/api/chat",
            "preview": "/api/preview/{video_id}",
            "export": "/api/export/{video_id}"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

