import { getExportUrl } from '../services/api';

function ExportButton({ videoId, disabled }) {
  const handleExport = () => {
    if (!videoId) return;
    
    const exportUrl = getExportUrl(videoId);
    window.open(exportUrl, '_blank');
  };

  return (
    <div className="export-section">
      <button
        onClick={handleExport}
        disabled={disabled || !videoId}
        className="export-button"
      >
        Export Final Video
      </button>
    </div>
  );
}

export default ExportButton;

