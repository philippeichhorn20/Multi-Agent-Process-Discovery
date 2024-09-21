import React, { useState } from 'react';
import VizViewer from './VizViewer';
import { parsePnmlToDot, parseJsonToDot } from '../Parser/dot_parser'; // Import the parser
import './Views.css';
import LeftScreenContent from './LeftScreen';
import StatView from './StatView'; // Import StatView
import {basic_miner} from '../DatabaseRequests'

const MainView = () => {
  const [file, setFile] = useState(null); // Track the uploaded file
  const [dotString, setDotString] = useState(''); // State for DOT string
  const [loading, setLoading] = useState(false); // State for loading animation
  const [miner, setMiner] = useState(''); // State for selected miner
  const [noiseThreshold, setNoiseThreshold] = useState(0); // State for noise threshold
  const [statistics, setStatistics] = useState({}); // State for statistics

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
    setLoading(true); // Start loading animation
    let result = await basic_miner(file, miner, noiseThreshold)
    console.log(result)
  
    if(result){
      setDotString(result.dotstring)
      setStatistics(result.stats)
    }
    setLoading(false); // Stop loading animation
  };

  const resetEverything = () => {
    setFile(null);
    setDotString('');
    setLoading(false);
    setMiner('');
    setNoiseThreshold(0);
    setStatistics({});
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
          <div className="divider"></div> {/* Added vertical divider */}
          <div className="right-screen">
            <StatView statistics={statistics} /> {/* Pass statistics to StatView */}
          </div>
        </div>
      </div>
      {file && dotString && <button style={{ position: 'absolute', top: '5%', left: '5%' }} onClick={resetEverything}>Reset Everything</button>} {/* Added reset button */}
    </div>
  );
};

export default MainView;