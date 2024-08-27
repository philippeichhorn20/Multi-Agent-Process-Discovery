import './App.css';
import React from 'react';
import MainView from './MainView';
import axios from 'axios';


axios.defaults.baseURL = 'http://localhost:8000';


function App() {
  return (
    <div className="App">
      <main>
        <MainView />
      </main>
    </div>
  );
}

export default App;
