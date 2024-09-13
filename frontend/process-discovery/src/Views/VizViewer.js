import React, { useEffect, useRef, useState } from 'react';
import { instance } from "@viz-js/viz";

const VizViewer = ({ dotString }) => {
  const [svg, setSvg] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const vizRef = useRef(null);
  const svgContainerRef = useRef(null); // Reference for the SVG container
  const [scale, setScale] = useState(1); // State for scaling

  const handleScaleChange = (increment) => {
    const newScale = scale + increment; // Adjust scale based on button click
    setScale(Math.min(Math.max(newScale, 0.1), 10)); // Limit scale between 0.5 and 3
  };

  const downloadSVG = () => {
    if (svg) {
      const blob = new Blob([svg.outerHTML], { type: 'image/svg+xml' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'graph.svg'; // Set the file name
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url); // Clean up
    }
  };

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
          svgElement.style.transform = 'scale(0.1)'; // Scale down the SVG to 10%
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

  useEffect(() => {
    if (svgContainerRef.current) {
      svgContainerRef.current.style.transform = `scale(${scale})`; // Apply scale to the container
    }
  }, [scale]);

  console.log('Current dotString:', dotString); // Debug log

  return (
    <div className="viz-viewer"> {/* Removed onTouchMove */}
      <button onClick={() => handleScaleChange(0.1)}>+</button> {/* Plus button */}
      <button onClick={() => handleScaleChange(-0.1)}>-</button> {/* Minus button */}
      <button onClick={downloadSVG}>Download SVG</button> {/* Download button */}
      {loading && <p>Loading graph...</p>}
      {error && <p className="error">{error}</p>}
      
      <div className="svg-container" ref={svgContainerRef} /> {/* Container for the SVG */}
      {!svg && !loading && !error && <p>No graph to display. Please provide a valid DOT string.</p>}
      {/*       <div className="dot-string-display">
        <h3>DOT String:</h3>
        <pre>{dotString}</pre>
      </div>*/}

    </div>
  );
};

export default VizViewer;
