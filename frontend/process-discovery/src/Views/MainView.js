import React, { useState } from 'react';
import VizViewer from './VizViewer';
import { parsePnmlToDot, parseJsonToDot } from '../Parser/dot_parser'; // Import the parser
import axios from 'axios'; // Import axios for API calls
import './Views.css';
import LeftScreenContent from './LeftScreen';

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
            <LeftScreenContent
              dotString={dotString}
              file={file}
              miner={miner}
              setMiner={setMiner}
              noiseThreshold={noiseThreshold}
              setNoiseThreshold={setNoiseThreshold}
              handleFileUpload={handleFileUpload}
              handleMinerSelection={handleMinerSelection}
              loading={loading}
            />
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