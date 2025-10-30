from fastapi import APIRouter, HTTPException
from app.models.video import ChatRequest, ChatResponse
from app.models.subtitle import SubtitleResponse
from app.langgraph_flows.subtitle_flow import parse_subtitle_prompt
from app.services.video_processor import burn_subtitles_to_video
from app.api.upload import video_sessions, OUTPUT_DIR
import os

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def process_chat(request: ChatRequest):
    """Process chat prompt and add subtitle to video"""
    
    # Check if video exists
    if request.video_id not in video_sessions:
        raise HTTPException(status_code=404, detail="Video not found")
    
    session = video_sessions[request.video_id]
    
    # Parse prompt using LangGraph + LLM
    try:
        subtitle_params = parse_subtitle_prompt(request.prompt, session.duration)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse prompt: {str(e)}")
    
    # Create subtitle object
    new_subtitle = SubtitleResponse(**subtitle_params)
    
    # Add to session
    session.subtitles.append(new_subtitle)
    
    # Generate output video with all subtitles
    output_filename = f"{request.video_id}_output.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    try:
        burn_subtitles_to_video(
            session.file_path,
            session.subtitles,
            output_path
        )
    except Exception as e:
        # Remove the subtitle that failed
        session.subtitles.pop()
        raise HTTPException(status_code=500, detail=f"Failed to process video: {str(e)}")
    
    # Update session with new output path
    session.file_path = output_path
    
    return ChatResponse(
        video_id=request.video_id,
        message="Subtitle added successfully",
        processed_video_url=f"/preview/{request.video_id}",
        subtitle_added=new_subtitle
    )

