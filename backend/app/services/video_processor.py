import ffmpeg
import os
from app.services.subtitle_generator import generate_ass_file
from app.models.subtitle import SubtitleResponse


def get_video_duration(video_path: str) -> float:
    """Get video duration in seconds using ffmpeg"""
    probe = ffmpeg.probe(video_path)
    duration = float(probe['format']['duration'])
    return duration


def burn_subtitles_to_video(
    input_video_path: str,
    subtitles: list[SubtitleResponse],
    output_video_path: str
) -> str:
    """Burn subtitles into video using FFmpeg with ASS format for styling"""
    
    # Generate ASS subtitle file with styling
    ass_file_path = output_video_path.replace('.mp4', '.ass')
    generate_ass_file(subtitles, ass_file_path)
    
    try:
        # Use FFmpeg to burn subtitles
        (
            ffmpeg
            .input(input_video_path)
            .output(
                output_video_path,
                vf=f"ass={ass_file_path}",
                vcodec='libx264',
                acodec='aac',
                strict='experimental'
            )
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        
        # Clean up ASS file
        if os.path.exists(ass_file_path):
            os.remove(ass_file_path)
        
        return output_video_path
    
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        raise Exception(f"Failed to process video: {e.stderr.decode()}")

