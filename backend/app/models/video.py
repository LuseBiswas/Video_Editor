from pydantic import BaseModel
from typing import List, Optional
from .subtitle import SubtitleResponse


class VideoSession(BaseModel):
    video_id: str
    original_filename: str
    file_path: str
    duration: Optional[float] = None
    subtitles: List[SubtitleResponse] = []


class VideoUploadResponse(BaseModel):
    video_id: str
    filename: str
    message: str


class ChatRequest(BaseModel):
    video_id: str
    prompt: str


class ChatResponse(BaseModel):
    video_id: str
    message: str
    processed_video_url: str
    subtitle_added: SubtitleResponse
