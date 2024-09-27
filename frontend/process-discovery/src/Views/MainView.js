import React, { useState } from 'react';
import { parsePnmlToDot } from '../Parser/dot_parser';
import './Views.css';
import LeftScreen from './LeftScreen';
import { run_miner } from '../DatabaseRequests';
import UploadView from './UploadView';

// Custom ErrorDialog component
const ErrorDialog = ({ isOpen, onClose, errorMessage }) => {
  if (!isOpen) return null;

  return (
    <div className="error-dialog-overlay">
      <div className="error-dialog">
        <h2>Error</h2>
        <p>errorMessage</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

const MainView = () => {
  const [file, setFile] = useState(null);
  const [dotString, setDotString] = useState('');
  const [abstractDotString, setAbstractDotString] = useState('');
  const [loading, setLoading] = useState(false);
  const [miner, setMiner] = useState('');
  const [noiseThreshold, setNoiseThreshold] = useState(0);
  const [statistics, setStatistics] = useState({});
  const [useCompositionalMethod, setUseCompositionalMethod] = useState(true);
  const [colors, setColors] = useState([]);
  const [resources, setResources] = useState([]);
  const [alignmentMetrics, setAlignmentMetrics] = useState(false);
  const [entropyMetrics, setEntropyMetrics] = useState(false);
  const [errorText, setErrorText] = useState('');
  const [isErrorDialogOpen, setIsErrorDialogOpen] = useState(false);

  const handleFileUpload = async (event) => {
    console.log("jnfk")

    const uploadedFile = event.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      const text = await uploadedFile.text();
      if (uploadedFile.name.endsWith('.pnml')) {
        const parsedDotString = parsePnmlToDot(text);
        setDotString(parsedDotString);
      } else if (uploadedFile.name.endsWith('.xes')) {
        setMiner('');
        setNoiseThreshold('');
      }
    }
  };

  const handleMinerSelection = async () => {
    setLoading(true);
    let result = await run_miner(file, miner, noiseThreshold, useCompositionalMethod, alignmentMetrics, entropyMetrics);
    console.log(result)

    if (typeof(result) == typeof("string")) {
      setErrorText(result);
      setIsErrorDialogOpen(true);
      resetEverything()
    }

    if (result) {
      setDotString(result.dotstring);
      setAbstractDotString(result.abstractedDotString);
      setStatistics(result.stats);
      setColors(result.colors);
      setResources(result.resources);
    }

    setLoading(false);
  };

  const resetEverything = () => {
    setFile(null);
    setDotString('');
    setAbstractDotString('');
    setLoading(false);
    setMiner('');
    setNoiseThreshold(0);
    setStatistics({});
  };

  const closeErrorDialog = () => {
    setIsErrorDialogOpen(false);
    setErrorText('');
  };

  return (
    <div className="main-view-container">
      <div className='header'>
        Compositional Miner
        <div style={{ display: 'flex', alignItems: 'center', fontSize: '10px', fontWeight: 'bold', color: '#6B6B6B', marginTop: '5px' }}>
          by Philipp Eichhorn • implementing&nbsp;<a href="https://doi.org/10.1007/s10270-022-01008-x" style={{ color: '#3366CC', textDecoration: 'underline' }}>Architecture aware sound Process Models</a>
        </div>
      </div>
      <div className='divider'></div>
      <div className="content">
        {!dotString && (
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
            setFile={setFile}
          />
        )}
        <div className="split-screen">
          {dotString && (
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
              colors={colors}
              resources={resources}
              setDotString={setDotString}
              setAbstractDotString={setAbstractDotString}
            />
          )}
        </div>
      </div>
      {file && dotString && <button style={{ position: 'absolute', bottom: '0', left: '45vw', margin: 10 }} onClick={resetEverything}>Reset Everything</button>}
      
      <ErrorDialog
        isOpen={isErrorDialogOpen}
        onClose={closeErrorDialog}
        errorMessage={errorText}
      />
    </div>
  );
};

export default MainView;