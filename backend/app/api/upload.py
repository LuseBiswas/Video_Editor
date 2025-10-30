from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.video import VideoUploadResponse, VideoSession
from app.services.video_processor import get_video_duration
import uuid
import os
import shutil

router = APIRouter()

# In-memory storage for video sessions (for MVP)
video_sessions = {}

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile = File(...)):
    """Upload a video file"""
    
    # Validate file type
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video")
    
    # Generate unique video ID
    video_id = str(uuid.uuid4())
    
    # Save file
    file_extension = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{video_id}{file_extension}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Get video duration
    try:
        duration = get_video_duration(file_path)
    except Exception as e:
        duration = None
    
    # Create video session
    session = VideoSession(
        video_id=video_id,
        original_filename=file.filename,
        file_path=file_path,
        duration=duration,
        subtitles=[]
    )
    
    video_sessions[video_id] = session
    
    return VideoUploadResponse(
        video_id=video_id,
        filename=file.filename,
        message="Video uploaded successfully"
    )


@router.get("/video/{video_id}")
async def get_video_info(video_id: str):
    """Get video session information"""
    
    if video_id not in video_sessions:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return video_sessions[video_id]

