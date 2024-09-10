import React, { useState } from 'react';
import VizViewer from './VizViewer';
import { parsePnmlToDot, parseJsonToDot } from '../Parser/dot_parser'; // Import the parser
import axios from 'axios'; // Import axios for API calls
import './Views.css';

const MainView = () => {
  const [file, setFile] = useState(null); // Track the uploaded file
  const [dotString, setDotString] = useState(''); // State for DOT string
  const [loading, setLoading] = useState(false); // State for loading animation
  const [miner, setMiner] = useState(''); // State for selected miner
  const [noiseThreshold, setNoiseThreshold] = useState(''); // State for noise threshold

  const handleFileUpload = async (event) => {
    const uploadedFile = event.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      const text = await uploadedFile.text(); // Read the file content
      if (uploadedFile.name.endsWith('.pnml')) {
        const parsedDotString = parsePnmlToDot(text); // Parse PNML to DOT
        setDotString(parsedDotString); // Set the DOT string
      } else if (uploadedFile.name.endsWith('.xes')) {
        // Reset miner and noise threshold for new file
        setMiner('');
        setNoiseThreshold('');
      }
    }
  };

  const handleMinerSelection = async () => {
    if (file && miner) {
      setLoading(true); // Start loading animation
      const formData = new FormData();
      formData.append('file', file);
      formData.append('algorithm', miner);
      if (miner === 'inductive') {
        formData.append('noise_threshold', noiseThreshold);
      }

      try {
        const response = await axios.post('http://localhost:8000/discover', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          responseType: 'text', // Expecting PNML format
          timeout: 60000,
          withCredentials: true,
        });
        const parsedDotString = parsePnmlToDot(response.data); // Parse PNML to DOT
        setDotString(parsedDotString);
      } catch (error) {
        console.error('Error during API call:', error);
      } finally {
        setLoading(false); // Stop loading animation
      }
    }
  };

  return (
    <div className="main-view-container">
      <div className="content">
        <div className="split-screen">
          <div className="left-screen">
            {dotString ? (
              <VizViewer dotString={dotString} /> // Pass the DOT string to VizViewer
            ) : (
              <div className="file-upload-button">
                <label>
                  <input type="file" accept=".pnml,.xes" onChange={handleFileUpload} style={{ display: 'none' }} />
                  <div className="large-file-icon">Upload File</div> {/* Large file icon/button */}
                </label>
              </div>
            )}
            {file && file.name.endsWith('.xes') && (
              <div>
                <h3>Select Miner</h3>
                <label>
                  <input type="radio" value="inductive" checked={miner === 'inductive'} onChange={() => setMiner('inductive')} />
                  Inductive Miner
                </label>
                <label>
                  <input type="radio" value="split" checked={miner === 'split'} onChange={() => setMiner('split')} />
                  Split Miner
                </label>
                {miner === 'inductive' && (
                  <div>
                    <label>
                      Noise Threshold:
                      <input type="number" value={noiseThreshold} onChange={(e) => setNoiseThreshold(e.target.value)} />
                    </label>
                  </div>
                )}
                <button onClick={handleMinerSelection}>Run Miner</button>
              </div>
            )}
            {loading && <div>Loading...</div>} {/* Loading animation */}
          </div>
          <div className="right-screen">
            <h2>Stats</h2>
            {/* Stats section will be added here */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainView;