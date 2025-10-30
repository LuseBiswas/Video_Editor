from fastapi import APIRouter, HTTPException
from app.models.video import ChatRequest, ChatResponse
from app.models.subtitle import SubtitleResponse
from app.langgraph_flows.subtitle_flow import parse_subtitle_prompt
from app.services.video_processor import burn_subtitles_to_video
from app.services.transcription_service import auto_generate_subtitles
from app.api.upload import video_sessions, OUTPUT_DIR
import os
import traceback

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def process_chat(request: ChatRequest):
    """Process chat prompt and add subtitle to video"""
    
    print(f"📥 Received prompt: {request.prompt}")
    
    # Check if video exists
    if request.video_id not in video_sessions:
        raise HTTPException(status_code=404, detail="Video not found")
    
    session = video_sessions[request.video_id]
    print(f"📹 Video duration: {session.duration}s")
    
    # Parse prompt using LangGraph + LLM
    try:
        subtitle_params = parse_subtitle_prompt(request.prompt, session.duration)
        print(f"✅ Parsed params: {subtitle_params}")
    except Exception as e:
        print(f"❌ Parse error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Failed to parse prompt: {str(e)}")
    
    auto_subtitles = []
    added_subtitles_count = 0
    
    # Check if auto-generate is requested
    if subtitle_params.get("auto_generate"):
        # Auto-generate subtitles from video audio
        try:
            auto_subtitles = auto_generate_subtitles(
                session.file_path,
                font_size=subtitle_params["font_size"],
                color=subtitle_params["color"],
                position=subtitle_params["position"]
            )
            
            # Add all generated subtitles to session
            session.subtitles.extend(auto_subtitles)
            added_subtitles_count = len(auto_subtitles)
            
            # Use first subtitle for response
            new_subtitle = auto_subtitles[0] if auto_subtitles else SubtitleResponse(
                text="(Auto-generated subtitles)",
                start_time=0,
                end_time=5,
                font_size=subtitle_params["font_size"],
                color=subtitle_params["color"],
                position=subtitle_params["position"]
            )
            
            message = f"Auto-generated {len(auto_subtitles)} subtitle segments from audio"
            
        except Exception as e:
            print(f"❌ Auto-generate error: {str(e)}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Failed to auto-generate subtitles: {str(e)}")
    else:
        # Manual subtitle with provided text
        print(f"📝 Creating manual subtitle")
        new_subtitle = SubtitleResponse(**subtitle_params)
        session.subtitles.append(new_subtitle)
        added_subtitles_count = 1
        message = "Subtitle added successfully"
    
    # Generate output video with all subtitles
    output_filename = f"{request.video_id}_output.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    print(f"🎬 Burning {len(session.subtitles)} subtitles to video...")
    try:
        burn_subtitles_to_video(
            session.file_path,
            session.subtitles,
            output_path
        )
        print(f"✅ Video processing complete!")
    except Exception as e:
        print(f"❌ Video processing error: {str(e)}")
        traceback.print_exc()
        # Remove the subtitles that failed
        if added_subtitles_count > 0:
            session.subtitles = session.subtitles[:-added_subtitles_count]
        raise HTTPException(status_code=500, detail=f"Failed to process video: {str(e)}")
    
    # Update session with new output path
    session.file_path = output_path
    
    return ChatResponse(
        video_id=request.video_id,
        message=message,
        processed_video_url=f"/preview/{request.video_id}",
        subtitle_added=new_subtitle
    )

