from pydantic import BaseModel, Field
from typing import Optional


class SubtitleRequest(BaseModel):
    text: str
    start_time: float = Field(default=0.0, description="Start time in seconds")
    end_time: Optional[float] = Field(default=None, description="End time in seconds")
    font_size: int = Field(default=24, description="Font size in pixels")
    color: str = Field(default="white", description="Font color")
    position: str = Field(default="bottom", description="Position: top, center, bottom")


class SubtitleResponse(BaseModel):
    text: str
    start_time: float
    end_time: float
    font_size: int
    color: str
    position: str
