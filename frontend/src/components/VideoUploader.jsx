import { useState } from 'react';
import { uploadVideo } from '../services/api';

function VideoUploader({ onVideoUploaded }) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('video/')) {
      setError('Please select a valid video file');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const result = await uploadVideo(file);
      onVideoUploaded(result.video_id, file.name);
    } catch (err) {
      setError('Failed to upload video: ' + err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="video-uploader">
      <h2>Upload Video</h2>
      <input
        type="file"
        accept="video/*"
        onChange={handleFileChange}
        disabled={uploading}
      />
      {uploading && <p className="loading">Uploading...</p>}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default VideoUploader;

