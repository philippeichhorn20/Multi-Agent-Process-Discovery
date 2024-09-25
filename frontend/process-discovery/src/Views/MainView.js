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
  const [alignmentMetrics, setAlignmentMetrics] = useState(false); // State for alignment metrics
  const [entropyMetrics, setEntropyMetrics] = useState(false); // State for entropy metrics


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
    let result = await run_miner(file, miner, noiseThreshold, useCompositionalMethod, alignmentMetrics, entropyMetrics)
  
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
      <div className='header'>
        Compositional Miner
        <div style={{ display: 'flex', alignItems: 'center', fontSize: '10px', fontWeight: 'bold', color: '#6B6B6B', marginTop: '5px' }}>
    by Philipp Eichhorn • implementing&nbsp;<a href="https://doi.org/10.1007/s10270-022-01008-x" style={{ color: '#3366CC', textDecoration: 'underline' }}>  Architecture aware sound Process Models</a>
</div>


      </div>
      <div className='divider'>

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
          alignmentMetrics={alignmentMetrics}
          setAlignmentMetrics={setAlignmentMetrics}
          entropyMetrics={entropyMetrics}
          setEntropyMetrics={setEntropyMetrics}
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
      {file && dotString && <button style={{ position: 'absolute', bottom: '0', left: '45vw', margin:10 }} onClick={resetEverything}>Reset Everything</button>} {/* Added reset button */}
    </div>
  );
};

export default MainView;