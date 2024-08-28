import React, { useState } from 'react';
import axios from 'axios';
import NetViewer from '../Views/NetViewer';
import { parsePnml, parseJson } from '../Parser/Parser';
import './Views.css';

const MainView = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [algorithm, setAlgorithm] = useState('split');
  const [noiseThreshold, setNoiseThreshold] = useState(0.2);
  const [isLoading, setIsLoading] = useState(false);
  const [netElements, setNetElements] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [key, setKey] = useState(0);
  const [netViewers, setNetViewers] = useState([]);
  const [activeNetViewerIndex, setActiveNetViewerIndex] = useState(0);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && (file.name.endsWith('.xes') || file.name.endsWith('.pnml'))) {
      setSelectedFile(file);
      console.log('Selected file:', file.name);
      if (file.name.endsWith('.pnml')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const content = e.target.result;
          visualizeNet(content, file.name);
        };
        reader.readAsText(file);
      }
    } else {
      alert('Please select a valid .xes or .pnml file');
    }
  };

  const handleAlgorithmChange = (event) => {
    setAlgorithm(event.target.value);
  };

  const handleNoiseThresholdChange = (event) => {
    setNoiseThreshold(parseFloat(event.target.value));
  };

  const handleDiscover = async () => {
    if (!selectedFile) {
      alert('Please select a file first');
      return;
    }

    if (selectedFile.name.endsWith('.pnml')) {
      // PNML file is already visualized, no need to discover
      return;
    }

    setIsLoading(true);
    setErrorMessage('');

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('algorithm', algorithm);
    if (algorithm === 'inductive') {
      formData.append('noise_threshold', noiseThreshold);
    }

    try {
      console.log('Sending discovery request...');
      const response = await axios.post('/discover', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'text',
        timeout: 60000,
        withCredentials: true,
      });
      console.log('Discovery response received');
      visualizeNet(response.data, selectedFile.name);
    } catch (error) {
      handleDiscoveryError(error);
    } finally {
      setIsLoading(false);
    }
  };

  const visualizeNet = (content, fileName) => {
    let netElements;
    if (content.startsWith('<?xml') || content.startsWith('<pnml')) {
      netElements = parsePnml(content);
    } else {
      netElements = parseJson(content);
    }
    const newNetViewer = { netElements, fileName };
    setNetViewers(prev => [...prev, newNetViewer]);
    setActiveNetViewerIndex(netViewers.length);
  };

  const handleDiscoveryError = (error) => {
    console.error('Error during discovery:', error);
    if (error.code === 'ERR_NETWORK') {
      setErrorMessage('Network error: The server might be taking too long to respond. Please try again or check with the administrator.');
    } else if (error.code === 'ECONNABORTED') {
      setErrorMessage('The request timed out. The process might be taking longer than expected. Please try again or use a smaller file.');
    } else if (error.response) {
      setErrorMessage(`Server error: ${error.response.data.message || 'Unknown error'}`);
    } else if (error.request) {
      setErrorMessage('No response received from server. The process might have completed on the server but failed to send the response.');
    } else {
      setErrorMessage(`An error occurred during discovery: ${error.message}`);
    }
  };

  const handleReload = () => {
    setKey(prevKey => prevKey + 1);
  };

  const handleCloseNetViewer = (index) => {
    setNetViewers(prev => prev.filter((_, i) => i !== index));
    if (activeNetViewerIndex === index) {
      setActiveNetViewerIndex(Math.max(0, index - 1));
    } else if (activeNetViewerIndex > index) {
      setActiveNetViewerIndex(prev => prev - 1);
    }
  };

  return (
    <div className="main-view-container">
      {isLoading && (
        <div className="loading-overlay">
          <div className="loading-spinner" />
        </div>
      )}
      <div className="header">
        <div>Process Discovery Tool</div>
        <div className="dropdown-container">
          <input
            type="file"
            id="xes-file-input"
            className="file-input"
            accept=".xes,.pnml"
            onChange={handleFileChange}
          />
          <label htmlFor="xes-file-input" className="dropdown-button">
            {selectedFile ? selectedFile.name : 'Upload XES or PNML File'}
          </label>
        </div>
      </div>
      <div className="content">
        <div className="sidebar">
          <div className="control-panel">
            <div className="algorithm-selector">
              <div>Select Algorithm:</div>
              <label>
                <input
                  type="radio"
                  className="radio-button"
                  value="split"
                  checked={algorithm === 'split'}
                  onChange={handleAlgorithmChange}
                />
                Split Miner
              </label>
              <label>
                <input
                  type="radio"
                  className="radio-button"
                  value="inductive"
                  checked={algorithm === 'inductive'}
                  onChange={handleAlgorithmChange}
                />
                Inductive Miner
              </label>
            </div>
            {algorithm === 'inductive' && (
              <div>
                <div>Noise Threshold: {noiseThreshold}</div>
                <input
                  type="range"
                  className="slider"
                  min="0"
                  max="1"
                  step="0.01"
                  value={noiseThreshold}
                  onChange={handleNoiseThresholdChange}
                />
              </div>
            )}
            <button 
              className="discover-button" 
              onClick={handleDiscover} 
              disabled={isLoading || !selectedFile || selectedFile.name.endsWith('.pnml')}
            >
              {isLoading ? 'Discovering...' : 'Discover Process'}
            </button>
            <button className="reload-button" onClick={handleReload}>
              Reload NetViewer
            </button>
            {errorMessage && <div className="error-message">{errorMessage}</div>}
          </div>
        </div>
        <div className="net-viewer-container">
          <div className="net-viewer-tabs">
            {netViewers.map((viewer, index) => (
              <div
                key={index}
                className={`net-viewer-tab ${index === activeNetViewerIndex ? 'active' : ''}`}
                onClick={() => setActiveNetViewerIndex(index)}
              >
                {viewer.fileName}
                <button onClick={(e) => { e.stopPropagation(); handleCloseNetViewer(index); }}>×</button>
              </div>
            ))}
          </div>
          {netViewers.map((viewer, index) => (
            <div
              key={index}
              className={`net-viewer-content ${index === activeNetViewerIndex ? 'active' : ''}`}
            >
              <NetViewer netElements={viewer.netElements} />
            </div>
          ))}
        </div>
      </div>
      <div className="footer">© 2023 Process Discovery Tool</div>
    </div>
  );
};

export default MainView;