from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.api.upload import video_sessions, OUTPUT_DIR
import os

router = APIRouter()


@router.get("/preview/{video_id}")
async def preview_video(video_id: str):
    """Get processed video for preview"""
    
    if video_id not in video_sessions:
        raise HTTPException(status_code=404, detail="Video not found")
    
    session = video_sessions[video_id]
    
    if not os.path.exists(session.file_path):
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(
        session.file_path,
        media_type="video/mp4",
        filename=f"preview_{session.original_filename}"
    )


@router.get("/export/{video_id}")
async def export_video(video_id: str):
    """Export final video with all subtitles burned in"""
    
    if video_id not in video_sessions:
        raise HTTPException(status_code=404, detail="Video not found")
    
    session = video_sessions[video_id]
    
    # Check if processed video exists
    output_path = os.path.join(OUTPUT_DIR, f"{video_id}_output.mp4")
    
    if not os.path.exists(output_path):
        # If no processing done yet, return original
        output_path = session.file_path
    
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(
        output_path,
        media_type="video/mp4",
        filename=f"final_{session.original_filename}",
        headers={"Content-Disposition": f"attachment; filename=final_{session.original_filename}"}
    )

