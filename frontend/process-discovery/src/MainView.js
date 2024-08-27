import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import NetViewer from './NetViewer';
import { parsePnml } from './PnmlParser';

const MainViewContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
`;

const Header = styled.div`
  height: 60px;
  border-bottom: 1px solid #ccc;
  display: flex;
  align-items: center;
  padding: 0 20px;
  justify-content: space-between;
`;

const Footer = styled.div`
  height: 40px;
  border-top: 1px solid #ccc;
  display: flex;
  align-items: center;
  padding: 0 20px;
`;

const Content = styled.div`
  flex: 1;
  display: flex;
`;

const Sidebar = styled.div`
  width: 250px;
  border-right: 1px solid #ccc;
  padding: 20px;
`;

const NetViewerContainer = styled.div`
  flex: 1;
  padding: 20px;
`;

const DropdownContainer = styled.div`
  position: relative;
`;

const FileInput = styled.input`
  display: none;
`;

const DropdownButton = styled.button`
  padding: 10px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
`;

const ControlPanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
`;

const AlgorithmSelector = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const RadioButton = styled.input`
  margin-right: 10px;
`;

const Slider = styled.input`
  width: 100%;
`;

const DiscoverButton = styled.button`
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  &:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
`;

const ReloadButton = styled.button`
  padding: 10px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
`;

const LoadingOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const LoadingSpinner = styled.div`
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const ErrorMessage = styled.div`
  color: red;
  margin-top: 10px;
`;

const MainView = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [algorithm, setAlgorithm] = useState('split');
  const [noiseThreshold, setNoiseThreshold] = useState(0.2);
  const [isLoading, setIsLoading] = useState(false);
  const [netElements, setNetElements] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [key, setKey] = useState(0);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.xes')) {
      setSelectedFile(file);
      console.log('Selected file:', file.name);
    } else {
      alert('Please select a valid .xes file');
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
      const pnmlContent = response.data;
      const netElements = parsePnml(pnmlContent);
      setNetElements(netElements);
    } catch (error) {
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
    } finally {
      setIsLoading(false);
    }
  };

  const handleReload = () => {
    setKey(prevKey => prevKey + 1);
  };

  return (
    <MainViewContainer>
      {isLoading && (
        <LoadingOverlay>
          <LoadingSpinner />
        </LoadingOverlay>
      )}
      <Header>
        <div>Process Discovery Tool</div>
        <DropdownContainer>
          <FileInput
            type="file"
            id="xes-file-input"
            accept=".xes"
            onChange={handleFileChange}
          />
          <DropdownButton as="label" htmlFor="xes-file-input">
            {selectedFile ? selectedFile.name : 'Upload XES File'}
          </DropdownButton>
        </DropdownContainer>
      </Header>
      <Content>
        <Sidebar>
          <ControlPanel>
            <AlgorithmSelector>
              <div>Select Algorithm:</div>
              <label>
                <RadioButton
                  type="radio"
                  value="split"
                  checked={algorithm === 'split'}
                  onChange={handleAlgorithmChange}
                />
                Split Miner
              </label>
              <label>
                <RadioButton
                  type="radio"
                  value="inductive"
                  checked={algorithm === 'inductive'}
                  onChange={handleAlgorithmChange}
                />
                Inductive Miner
              </label>
            </AlgorithmSelector>
            {algorithm === 'inductive' && (
              <div>
                <div>Noise Threshold: {noiseThreshold}</div>
                <Slider
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={noiseThreshold}
                  onChange={handleNoiseThresholdChange}
                />
              </div>
            )}
            <DiscoverButton onClick={handleDiscover} disabled={isLoading || !selectedFile}>
              {isLoading ? 'Discovering...' : 'Discover Process'}
            </DiscoverButton>
            <ReloadButton onClick={handleReload}>
              Reload NetViewer
            </ReloadButton>
            {errorMessage && <ErrorMessage>{errorMessage}</ErrorMessage>}
          </ControlPanel>
        </Sidebar>
        <NetViewerContainer>
          <NetViewer key={key} netElements={netElements} />
        </NetViewerContainer>
      </Content>
      <Footer>© 2023 Process Discovery Tool</Footer>
    </MainViewContainer>
  );
};

export default MainView;