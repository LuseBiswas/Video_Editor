import { useState } from 'react';
import { sendChatMessage } from '../services/api';

function ChatInterface({ videoId, onSubtitleAdded }) {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [messages, setMessages] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim() || !videoId) return;

    setLoading(true);
    setError(null);

    // Add user message to chat
    setMessages([...messages, { type: 'user', text: prompt }]);

    try {
      const result = await sendChatMessage(videoId, prompt);
      
      // Add bot response
      setMessages(prev => [...prev, { 
        type: 'bot', 
        text: result.message,
        subtitle: result.subtitle_added 
      }]);
      
      onSubtitleAdded(result);
      setPrompt('');
    } catch (err) {
      setError('Failed to process: ' + err.message);
      setMessages(prev => [...prev, { type: 'error', text: 'Error: ' + err.message }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <h2>Add Subtitles via Chat</h2>
      
      <div className="chat-messages">
        {messages.length === 0 && (
          <p className="hint">
            Try: "add subtitle 'Hello World' at 5 seconds, 26px, red color"
          </p>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.type}`}>
            <strong>{msg.type === 'user' ? 'You' : 'Bot'}:</strong> {msg.text}
            {msg.subtitle && (
              <div className="subtitle-info">
                <small>
                  "{msg.subtitle.text}" | {msg.subtitle.start_time}s-{msg.subtitle.end_time}s | 
                  {msg.subtitle.font_size}px | {msg.subtitle.color}
                </small>
              </div>
            )}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="chat-input">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type your subtitle command..."
          disabled={loading || !videoId}
        />
        <button type="submit" disabled={loading || !videoId}>
          {loading ? 'Processing...' : 'Send'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default ChatInterface;

