# 🎬 Video Editor - Chat-Based Subtitle Generator

A full-stack web application that allows users to add subtitles to videos using natural language prompts. Built with FastAPI, React, and powered by LangGraph for LLM orchestration and OpenAI Whisper for automatic subtitle generation.

## ✨ Features

- 📤 **Video Upload** - Upload video files (MP4, AVI, MOV)
- 💬 **Chat Interface** - Add subtitles using natural language commands
- 🎨 **Custom Styling** - Control font size, color, and position
- 🤖 **Auto-Generate Subtitles** - AI-powered speech-to-text transcription
- 🎥 **Real-time Preview** - See changes immediately
- 💾 **Export Video** - Download final video with burned-in subtitles

## 🚀 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain + LangGraph** - LLM orchestration and workflow management
- **OpenAI GPT-3.5** - Natural language prompt parsing
- **OpenAI Whisper** - Automatic speech-to-text transcription
- **FFmpeg** - Video processing and subtitle burning
- **Pydantic** - Data validation

### Frontend
- **React** - UI framework
- **Vite** - Fast build tool
- **Axios** - HTTP client
- **CSS** - Custom styling

## 📋 Prerequisites

- Python 3.12+
- Node.js 16+
- FFmpeg (for video processing)
- OpenAI API Key

## 🛠️ Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd Video_Editor
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg (if not already installed)
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

## 🚀 Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Backend will run on: `http://localhost:8000`

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will run on: `http://localhost:3000`

## 📖 Usage

### 1. Upload Video
- Click "Choose File" and select a video
- Video will be uploaded and processed

### 2. Add Subtitles via Chat

#### Manual Subtitle (with specific text):
```
"add subtitle 'Hello World' at 5 seconds, 26px, red"
"show 'Welcome' in blue, 30px at top"
"add 'Testing' from 2 to 8 seconds"
```

#### Auto-Generate Subtitles (from audio):
```
"make subtitle green of 36px"
"generate subtitles in red, 30px"
"add subtitles from audio, blue color"
```

### 3. Preview & Export
- Video preview updates automatically
- Click "Export Final Video" to download

## 🎨 Styling Options

| Property | Options | Example |
|----------|---------|---------|
| **Font Size** | Any px value | `26px`, `36px` |
| **Color** | white, red, blue, green, yellow, black, orange, pink | `red`, `green` |
| **Position** | top, center, bottom | `at top` |
| **Timing** | Seconds | `at 5 seconds`, `from 2 to 8 seconds` |

## 📁 Project Structure

```
Video_Editor/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── upload.py       # Video upload endpoint
│   │   │   ├── chat.py         # Chat/prompt processing
│   │   │   └── export.py       # Video preview/export
│   │   ├── services/
│   │   │   ├── video_processor.py          # FFmpeg video processing
│   │   │   ├── subtitle_generator.py       # SRT/ASS file generation
│   │   │   └── transcription_service.py    # Whisper transcription
│   │   ├── langgraph_flows/
│   │   │   └── subtitle_flow.py           # LLM prompt parsing with LangGraph
│   │   ├── models/
│   │   │   ├── subtitle.py     # Subtitle data models
│   │   │   └── video.py        # Video data models
│   │   └── main.py             # FastAPI app entry point
│   ├── uploads/                # Temporary video storage
│   ├── outputs/                # Processed videos
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── VideoUploader.jsx    # Video upload UI
    │   │   ├── ChatInterface.jsx    # Chat interface
    │   │   ├── VideoPreview.jsx     # Video player
    │   │   └── ExportButton.jsx     # Export button
    │   ├── services/
    │   │   └── api.js               # API client
    │   ├── App.jsx                  # Main app component
    │   └── main.jsx                 # React entry point
    ├── package.json
    └── vite.config.js
```

## 🔌 API Endpoints

### Upload Video
```http
POST /api/upload
Content-Type: multipart/form-data

Response:
{
  "video_id": "uuid",
  "filename": "video.mp4",
  "message": "Video uploaded successfully"
}
```

### Process Chat Prompt
```http
POST /api/chat
Content-Type: application/json

{
  "video_id": "uuid",
  "prompt": "make subtitle green of 36px"
}

Response:
{
  "video_id": "uuid",
  "message": "Auto-generated 15 subtitle segments from audio",
  "processed_video_url": "/preview/uuid",
  "subtitle_added": {
    "text": "Hello world",
    "start_time": 0.0,
    "end_time": 5.2,
    "font_size": 36,
    "color": "green",
    "position": "bottom"
  }
}
```

### Preview Video
```http
GET /api/preview/{video_id}

Response: Video stream
```

### Export Video
```http
GET /api/export/{video_id}

Response: Video file download
```

## 🧠 How It Works

### Workflow

```
1. User uploads video
   ↓
2. User sends prompt: "make subtitle green of 36px"
   ↓
3. LangGraph orchestrates LLM (GPT-3.5) to parse prompt
   ↓
4. If auto-generate requested:
   - Extract audio from video (FFmpeg)
   - Transcribe speech to text (Whisper AI)
   - Generate subtitle segments with timestamps
   ↓
5. Generate ASS subtitle file with styling
   ↓
6. Burn subtitles into video (FFmpeg)
   ↓
7. Return processed video for preview/export
```

### LangGraph Flow

```
User Prompt
    ↓
parse_prompt_with_llm (LLM extracts parameters)
    ↓
validate_parameters (Business logic validation)
    ↓
Decision: Error or Success?
    ↓
Return structured data
```

## 🎯 Key Technologies Explained

### Why LangGraph?
- **Orchestrates complex LLM workflows** as state graphs
- **Separates concerns**: LLM logic → Validation → Routing
- **Easy to extend** with new nodes and conditional flows
- **Built-in state management** and error handling

### Why Whisper?
- **OpenAI's speech-to-text model**
- **High accuracy** transcription
- **Automatic timestamps** for subtitle segments
- **Works offline** (model cached locally)

### Why FFmpeg?
- **Industry standard** for video processing
- **Burn subtitles** permanently into video
- **Extract audio** for transcription
- **Cross-platform** support

## 🐛 Troubleshooting

### SSL Certificate Error (Whisper Download)
```python
# Already fixed in transcription_service.py
ssl._create_default_https_context = ssl._create_unverified_context
```

### FFmpeg Not Found
```bash
# Install FFmpeg first
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Linux
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

## 📝 Environment Variables

Create `.env` file in `backend/` directory:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
PORT=8000
HOST=0.0.0.0
```

## 🎓 Assignment Requirements

✅ Full-stack application with FastAPI and React  
✅ Chat-based interface for video editing  
✅ Subtitle overlay with customizable styling  
✅ LangGraph for LLM orchestration  
✅ Video processing and export functionality  

## 📄 License

This project is created for educational/assignment purposes.

## 👨‍💻 Author

Created as an assignment project demonstrating:
- FastAPI backend development
- React frontend development
- LLM integration with LangChain/LangGraph
- Video processing with FFmpeg
- AI-powered speech-to-text with Whisper

---

**Made with ❤️ using FastAPI, React, LangGraph, and OpenAI**

