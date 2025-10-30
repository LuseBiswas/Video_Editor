from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
import json
import os
from dotenv import load_dotenv

load_dotenv()


class SubtitleState(TypedDict):
    prompt: str
    video_duration: float
    text: Optional[str]
    start_time: Optional[float]
    end_time: Optional[float]
    font_size: Optional[int]
    color: Optional[str]
    position: Optional[str]
    error: Optional[str]


def parse_prompt_with_llm(state: SubtitleState) -> SubtitleState:
    """Use LLM to parse user prompt and extract subtitle parameters"""
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    system_prompt = f"""You are a subtitle parameter extractor. 
Extract subtitle information from the user's prompt and return a JSON object with these fields:
- text: The subtitle text (required)
- start_time: Start time in seconds (default: 0)
- end_time: End time in seconds (default: video_duration or start_time + 5)
- font_size: Font size in pixels (default: 24)
- color: Color name (default: "white")
- position: Position - "top", "center", or "bottom" (default: "bottom")

Video duration is: {state['video_duration']} seconds

Examples:
- "add subtitle 'Hello World' at 5 seconds, 26px, red" -> {{"text": "Hello World", "start_time": 5, "end_time": 10, "font_size": 26, "color": "red", "position": "bottom"}}
- "show 'Welcome' in blue, 30px at top" -> {{"text": "Welcome", "start_time": 0, "end_time": 5, "font_size": 30, "color": "blue", "position": "top"}}
- "add 'Testing' from 2 to 8 seconds" -> {{"text": "Testing", "start_time": 2, "end_time": 8, "font_size": 24, "color": "white", "position": "bottom"}}

Return ONLY valid JSON, nothing else."""

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=state["prompt"])
        ]
        
        response = llm.invoke(messages)
        result = json.loads(response.content)
        
        state["text"] = result.get("text")
        state["start_time"] = result.get("start_time", 0)
        state["end_time"] = result.get("end_time", state["start_time"] + 5)
        state["font_size"] = result.get("font_size", 24)
        state["color"] = result.get("color", "white")
        state["position"] = result.get("position", "bottom")
        state["error"] = None
        
    except Exception as e:
        state["error"] = f"Failed to parse prompt: {str(e)}"
    
    return state


def validate_parameters(state: SubtitleState) -> SubtitleState:
    """Validate extracted parameters"""
    
    if not state.get("text"):
        state["error"] = "No subtitle text found in prompt"
        return state
    
    # Ensure end_time is after start_time
    if state["end_time"] <= state["start_time"]:
        state["end_time"] = state["start_time"] + 5
    
    # Clamp to video duration
    if state["end_time"] > state["video_duration"]:
        state["end_time"] = state["video_duration"]
    
    return state


def should_continue(state: SubtitleState) -> str:
    """Decide whether to continue or end"""
    if state.get("error"):
        return "error"
    return "success"


# Build the LangGraph workflow
def create_subtitle_parser_graph():
    workflow = StateGraph(SubtitleState)
    
    # Add nodes
    workflow.add_node("parse", parse_prompt_with_llm)
    workflow.add_node("validate", validate_parameters)
    
    # Define edges
    workflow.set_entry_point("parse")
    workflow.add_edge("parse", "validate")
    workflow.add_conditional_edges(
        "validate",
        should_continue,
        {
            "success": END,
            "error": END
        }
    )
    
    return workflow.compile()


# Create the graph instance
subtitle_parser = create_subtitle_parser_graph()


def parse_subtitle_prompt(prompt: str, video_duration: float) -> dict:
    """Main function to parse subtitle prompt using LangGraph"""
    
    initial_state = SubtitleState(
        prompt=prompt,
        video_duration=video_duration,
        text=None,
        start_time=None,
        end_time=None,
        font_size=None,
        color=None,
        position=None,
        error=None
    )
    
    result = subtitle_parser.invoke(initial_state)
    
    if result.get("error"):
        raise ValueError(result["error"])
    
    return {
        "text": result["text"],
        "start_time": result["start_time"],
        "end_time": result["end_time"],
        "font_size": result["font_size"],
        "color": result["color"],
        "position": result["position"]
    }

