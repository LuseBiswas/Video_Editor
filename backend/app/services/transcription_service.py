import whisper
import ffmpeg
import os
import ssl
import urllib.request
from typing import List
from app.models.subtitle import SubtitleResponse

# Fix SSL certificate verification issue for Whisper model download
ssl._create_default_https_context = ssl._create_unverified_context


def extract_audio_from_video(video_path: str, audio_output_path: str) -> str:
    """Extract audio from video file"""
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_output_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return audio_output_path
    except ffmpeg.Error as e:
        print(f"FFmpeg error during audio extraction: {e.stderr.decode()}")
        raise Exception(f"Failed to extract audio: {e.stderr.decode()}")


def transcribe_audio_to_subtitles(
    audio_path: str,
    font_size: int = 24,
    color: str = "white",
    position: str = "bottom"
) -> List[SubtitleResponse]:
    """Transcribe audio using Whisper and return subtitle segments"""
    
    # Load Whisper model (using base model for speed, can upgrade to 'medium' or 'large' for accuracy)
    model = whisper.load_model("base")
    
    # Transcribe with word-level timestamps
    result = model.transcribe(audio_path, word_timestamps=False)
    
    # Convert segments to SubtitleResponse objects
    subtitles = []
    for segment in result['segments']:
        subtitle = SubtitleResponse(
            text=segment['text'].strip(),
            start_time=segment['start'],
            end_time=segment['end'],
            font_size=font_size,
            color=color,
            position=position
        )
        subtitles.append(subtitle)
    
    return subtitles


def auto_generate_subtitles(
    video_path: str,
    font_size: int = 24,
    color: str = "white",
    position: str = "bottom"
) -> List[SubtitleResponse]:
    """Main function to auto-generate subtitles from video"""
    
    # Create temporary audio file
    audio_path = video_path.replace('.mp4', '_audio.wav')
    
    try:
        # Extract audio
        extract_audio_from_video(video_path, audio_path)
        
        # Transcribe
        subtitles = transcribe_audio_to_subtitles(audio_path, font_size, color, position)
        
        # Clean up audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        return subtitles
    
    except Exception as e:
        # Clean up on error
        if os.path.exists(audio_path):
            os.remove(audio_path)
        raise e

