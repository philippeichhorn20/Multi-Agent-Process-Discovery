import React, { useState } from 'react';
import axios from 'axios';
import NetViewer from '../Views/NetViewer';
import { parsePnml, parseJson } from '../Parser/Parser';
import './Views.css';

const MainView = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [algorithm, setAlgorithm] = useState('inductive');
  const [noiseThreshold, setNoiseThreshold] = useState(0.0);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [key, setKey] = useState(0);
  const [netViewers, setNetViewers] = useState([]);
  const [activeNetViewerIndex, setActiveNetViewerIndex] = useState(0);
  const [showAlgorithmDialog, setShowAlgorithmDialog] = useState(false);
  const [selectedNets, setSelectedNets] = useState([]);
  const [isomorphismResult, setIsomorphismResult] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && (file.name.endsWith('.xes') || file.name.endsWith('.pnml'))) {
      setSelectedFile(file);
      if (file.name.endsWith('.xes')) {
        setShowAlgorithmDialog(true);
      } else {
        setSelectedFile(file);
        console.log('Selected file:', file.name);
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
      console.log('No file selected');
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

  const handleAlgorithmDialogClose = () => {
    setShowAlgorithmDialog(false);
    setSelectedFile(null);
  };

  const handleAlgorithmSelect = () => {
    console.log('Selected file:', selectedFile.name);
    setShowAlgorithmDialog(false);
    handleDiscover();
    setSelectedFile(null);
  };

  const handleNetSelection = (index) => {
    setSelectedNets(prev => {
      if (prev.includes(index)) {
        return prev.filter(i => i !== index);
      } else if (prev.length < 2) {
        return [...prev, index];
      }
      return prev;
    });
  };

  const checkIsomorphism = async () => {
    if (selectedNets.length !== 2) {
      alert('Please select exactly two Petri nets to compare.');
      return;
    }

    setIsLoading(true);
    setErrorMessage('');

    try {
      const formData = new FormData();
      formData.append('file1', new Blob([JSON.stringify(netViewers[selectedNets[0]].netElements)], {type: 'application/json'}));
      formData.append('file2', new Blob([JSON.stringify(netViewers[selectedNets[1]].netElements)], {type: 'application/json'}));

      const response = await axios.post('/check_isomorphism', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        withCredentials: true,
      });

      setIsomorphismResult(response.data.isomorphic);
    } catch (error) {
      console.error('Error checking isomorphism:', error);
      setErrorMessage('An error occurred while checking isomorphism.');
    } finally {
      setIsLoading(false);
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
        <div className="control-panel">
            {errorMessage && <div className="error-message">{errorMessage}</div>}
          </div>
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
          <h3>Compare Petri Nets</h3>
          {netViewers.map((viewer, index) => (
            <div key={index} className="net-selector">
              <input
                type="checkbox"
                id={`net-${index}`}
                checked={selectedNets.includes(index)}
                onChange={() => handleNetSelection(index)}
                disabled={selectedNets.length === 2 && !selectedNets.includes(index)}
              />
              <label htmlFor={`net-${index}`}>{viewer.fileName}</label>
            </div>
          ))}
          <button onClick={checkIsomorphism} disabled={selectedNets.length !== 2}>
            Check Isomorphism
          </button>
          {isomorphismResult !== null && (
            <div className="isomorphism-result">
              The selected Petri nets are {isomorphismResult ? '' : 'not '}isomorphic.
            </div>
          )}
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
      {showAlgorithmDialog && (
        <div className="algorithm-dialog-overlay" style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0, 0, 0, 0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
          <div className="algorithm-dialog" style={{ backgroundColor: 'white', padding: '20px', borderRadius: '5px', boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)' }}>
            <h2>Select Algorithm</h2>
            <div>
              <label>
                <input
                  type="radio"
                  value="split"
                  checked={algorithm === 'split'}
                  onChange={handleAlgorithmChange}
                />
                Split Miner
              </label>
              <label>
                <input
                  type="radio"
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
                  min="0"
                  max="1"
                  step="0.01"
                  value={noiseThreshold}
                  onChange={handleNoiseThresholdChange}
                />
              </div>
            )}
            <div className="algorithm-dialog-buttons">
              <button onClick={handleAlgorithmDialogClose}>Cancel</button>
              <button onClick={handleAlgorithmSelect}>Confirm</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MainView;