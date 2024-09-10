import React, { useEffect, useRef, useState } from 'react';
import { instance } from "@viz-js/viz";

const VizViewer = ({ dotString }) => {
  const [svg, setSvg] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const vizRef = useRef(null);
  const svgContainerRef = useRef(null); // Reference for the SVG container

  useEffect(() => {
    instance().then(viz => {
      vizRef.current = viz;
      renderGraph(viz); // Call renderGraph with the viz instance
    });
  }, []);

  const renderGraph = async (viz) => {
    if (viz && dotString) {
      setLoading(true);
      setError(null);
      try {
        const svgElement = await viz.renderSVGElement(dotString);
        setSvg(svgElement);
        if (svgContainerRef.current) {
          svgContainerRef.current.innerHTML = ''; // Clear previous SVG
          svgElement.style.transform = 'scale(0.2)'; // Scale down the SVG to 10%
          svgElement.style.transformOrigin = '0 0'; // Set the origin for scaling
          svgContainerRef.current.appendChild(svgElement); // Append new SVG
        }
        console.log('SVG generated:', svgElement); // Debug log
      } catch (error) {
        console.error('Error rendering graph:', error);
        setError('Failed to render graph. Please check your DOT string.');
      } finally {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    if (vizRef.current) {
      renderGraph(vizRef.current); // Re-render when dotString changes
    }
  }, [dotString]);

  console.log('Current dotString:', dotString); // Debug log

  return (
    <div className="viz-viewer">
      {loading && <p>Loading graph...</p>}
      {error && <p className="error">{error}</p>}
      
      <div ref={svgContainerRef} /> {/* Container for the SVG */}
      {!svg && !loading && !error && <p>No graph to display. Please provide a valid DOT string.</p>}
      {/*       <div className="dot-string-display">
        <h3>DOT String:</h3>
        <pre>{dotString}</pre>
      </div>*/}

    </div>
  );
};

export default VizViewer;
