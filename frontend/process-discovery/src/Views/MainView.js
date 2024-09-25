import React, { useState } from 'react';
import VizViewer from './VizViewer';
import { parsePnmlToDot, parseJsonToDot } from '../Parser/dot_parser'; // Import the parser
import './Views.css';
import LeftScreen from './LeftScreen';
import StatView from './StatView'; // Import StatView
import { run_miner } from '../DatabaseRequests'
import UploadView from './UploadView'

const MainView = () => {
  const [file, setFile] = useState(null); // Track the uploaded file
  const [dotString, setDotString] = useState(''); // State for DOT string
  const [abstractDotString, setAbstractDotString] = useState(''); // State for DOT string
  const [loading, setLoading] = useState(false); // State for loading animation
  const [miner, setMiner] = useState(''); // State for selected miner
  const [noiseThreshold, setNoiseThreshold] = useState(0); // State for noise threshold
  const [statistics, setStatistics] = useState({}); // State for statistics
  const [useCompositionalMethod, setUseCompositionalMethod] = useState(true);
  const [colors, setColors] = useState([]); // State for colors
  const [resources, setResources] = useState([]); // State for resources

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
    let result = await run_miner(file, miner, noiseThreshold, useCompositionalMethod)
  
    if(result){
      setDotString(result.dotstring)
      setAbstractDotString(result.abstractedDotString)
      setStatistics(result.stats)
      setColors(result.colors)
      setResources(result.resources)
    }

    setLoading(false); // Stop loading animation
  };

  const resetEverything = () => {
    setFile(null);
    setDotString('');
    setAbstractDotString('')
    setLoading(false);
    setMiner('');
    setNoiseThreshold(0);
    setStatistics({});
  };

  return (
    <div className="main-view-container">
      <div>
        Compositional Miner
      </div>
      <div className="content">
        {
          !dotString &&
          <UploadView
          file={file}
          miner={miner}
          setMiner={setMiner}
          noiseThreshold={noiseThreshold}
          setNoiseThreshold={setNoiseThreshold}
          handleFileUpload={handleFileUpload}
          handleMinerSelection={handleMinerSelection}
          loading={loading}
          setUseCompositionalMethod={setUseCompositionalMethod}
          useCompositionalMethod={useCompositionalMethod}
          />
        }
        <div className="split-screen">
           {
            dotString &&
            <LeftScreen
            dotString={dotString}
            abstractDotString={abstractDotString}
            file={file}
            miner={miner}
            setMiner={setMiner}
            noiseThreshold={noiseThreshold}
            setNoiseThreshold={setNoiseThreshold}
            handleFileUpload={handleFileUpload}
            handleMinerSelection={handleMinerSelection}
            loading={loading}
            setUseCompositionalMethod={setUseCompositionalMethod}
            useCompositionalMethod={useCompositionalMethod}
            statistics={statistics}
            colors = {colors}
            resources = {resources}
            setDotString = {setDotString}
            setAbstractDotString = {setAbstractDotString}
          />
           }
        </div>
      </div>
      {file && dotString && <button style={{ position: 'absolute', top: '5%', left: '10px' }} onClick={resetEverything}>Reset Everything</button>} {/* Added reset button */}
    </div>
  );
};

export default MainView;