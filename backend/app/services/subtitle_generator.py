from datetime import timedelta
from app.models.subtitle import SubtitleResponse


def format_srt_time(seconds: float) -> str:
    """Convert seconds to SRT time format: HH:MM:SS,mmm"""
    td = timedelta(seconds=seconds)
    hours = int(td.total_seconds() // 3600)
    minutes = int((td.total_seconds() % 3600) // 60)
    secs = int(td.total_seconds() % 60)
    millis = int((td.total_seconds() % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def generate_srt_file(subtitles: list[SubtitleResponse], output_path: str) -> str:
    """Generate SRT subtitle file from subtitle data"""
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, subtitle in enumerate(subtitles, start=1):
            f.write(f"{idx}\n")
            f.write(f"{format_srt_time(subtitle.start_time)} --> {format_srt_time(subtitle.end_time)}\n")
            f.write(f"{subtitle.text}\n\n")
    
    return output_path


def generate_ass_style(font_size: int, color: str, position: str) -> str:
    """Generate ASS subtitle style with custom font size and color"""
    # Convert color name to ASS color format (BGR hex)
    color_map = {
        "white": "&H00FFFFFF",
        "red": "&H000000FF",
        "blue": "&H00FF0000",
        "green": "&H0000FF00",
        "yellow": "&H0000FFFF",
        "black": "&H00000000",
        "orange": "&H000099FF",
        "pink": "&H00FF00FF",
    }
    ass_color = color_map.get(color.lower(), "&H00FFFFFF")
    
    # Position alignment (1-9 numpad style)
    alignment_map = {
        "bottom": "2",  # Bottom center
        "center": "5",  # Center
        "top": "8",     # Top center
    }
    alignment = alignment_map.get(position.lower(), "2")
    
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,{font_size},{ass_color},&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2,1,{alignment},10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def format_ass_time(seconds: float) -> str:
    """Convert seconds to ASS time format: H:MM:SS.cc"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centisecs = int((seconds % 1) * 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{centisecs:02d}"


def generate_ass_file(subtitles: list[SubtitleResponse], output_path: str) -> str:
    """Generate ASS subtitle file with custom styling"""
    if not subtitles:
        return output_path
    
    # Use the first subtitle's style for the file
    first_sub = subtitles[0]
    content = generate_ass_style(first_sub.font_size, first_sub.color, first_sub.position)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
        for subtitle in subtitles:
            start = format_ass_time(subtitle.start_time)
            end = format_ass_time(subtitle.end_time)
            f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{subtitle.text}\n")
    
    return output_path

