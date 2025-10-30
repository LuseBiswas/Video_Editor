import { useState, useEffect } from 'react';
import { getPreviewUrl } from '../services/api';

function VideoPreview({ videoId }) {
  const [videoUrl, setVideoUrl] = useState(null);
  const [key, setKey] = useState(0);

  useEffect(() => {
    if (videoId) {
      setVideoUrl(getPreviewUrl(videoId));
      // Force video reload by changing key
      setKey(prev => prev + 1);
    }
  }, [videoId]);

  if (!videoUrl) {
    return (
      <div className="video-preview">
        <p>No video to preview yet</p>
      </div>
    );
  }

  return (
    <div className="video-preview">
      <h2>Video Preview</h2>
      <video
        key={key}
        controls
        width="100%"
        src={videoUrl}
      >
        Your browser does not support the video tag.
      </video>
    </div>
  );
}

export default VideoPreview;

