import { useState } from 'react';
import VideoUploader from './components/VideoUploader';
import ChatInterface from './components/ChatInterface';
import VideoPreview from './components/VideoPreview';
import ExportButton from './components/ExportButton';
import './App.css';

function App() {
  const [videoId, setVideoId] = useState(null);
  const [videoName, setVideoName] = useState('');
  const [previewKey, setPreviewKey] = useState(0);

  const handleVideoUploaded = (id, name) => {
    setVideoId(id);
    setVideoName(name);
    setPreviewKey(prev => prev + 1);
  };

  const handleSubtitleAdded = (result) => {
    // Trigger video preview refresh
    setPreviewKey(prev => prev + 1);
  };

  return (
    <div className="app">
      <header>
        <h1>🎬 Video Editor - Chat Based Subtitles</h1>
        {videoName && <p className="video-name">Current Video: {videoName}</p>}
      </header>

      <div className="container">
        <div className="left-panel">
          <VideoUploader onVideoUploaded={handleVideoUploaded} />
          <ChatInterface 
            videoId={videoId} 
            onSubtitleAdded={handleSubtitleAdded}
          />
          <ExportButton videoId={videoId} disabled={!videoId} />
        </div>

        <div className="right-panel">
          <VideoPreview key={previewKey} videoId={videoId} />
        </div>
      </div>
    </div>
  );
}

export default App;
