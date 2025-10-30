import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const uploadVideo = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const sendChatMessage = async (videoId, prompt) => {
  const response = await axios.post(`${API_BASE_URL}/chat`, {
    video_id: videoId,
    prompt: prompt,
  });
  
  return response.data;
};

export const getPreviewUrl = (videoId) => {
  return `${API_BASE_URL}/preview/${videoId}`;
};

export const getExportUrl = (videoId) => {
  return `${API_BASE_URL}/export/${videoId}`;
};

