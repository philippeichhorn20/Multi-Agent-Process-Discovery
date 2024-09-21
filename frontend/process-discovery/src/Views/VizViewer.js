import React, { useEffect, useRef, useState } from 'react';
import { instance } from "@viz-js/viz";

const VizViewer = ({ dotString }) => {
  const [svg, setSvg] = useState(null);
  const vizRef = useRef(null);
  const svgContainerRef = useRef(null);
  const [zoomLevel, setZoomLevel] = useState(1);

  const renderGraph = async (viz) => {
    if (viz && dotString) {
      try {
        const svgElement = await viz.renderSVGElement(dotString);
        setSvg(svgElement);
        if (svgContainerRef.current) {
          svgContainerRef.current.innerHTML = ''; // Clear previous SVG
          svgContainerRef.current.appendChild(svgElement); // Append new SVG
          // Adjust SVG to fit the container
          svgElement.setAttribute('width', '100%');
          svgElement.setAttribute('height', '100%');
          svgElement.setAttribute('preserveAspectRatio', 'xMidYMid meet');
        }
      } catch (error) {
        console.error('Error rendering graph:', error);
      }
    }
  };

  useEffect(() => {
    instance().then(viz => {
      renderGraph(viz); // Call renderGraph with the viz instance
    });
  }, []);

  useEffect(() => {
    if (svg) {
      // Adjust SVG to fit the container on scale change
      svg.setAttribute('width', '100%');
      svg.setAttribute('height', '100%');
      svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    } else {
      renderGraph(vizRef.current); // Re-render the graph when scale changes
    }
  }, [dotString]);

  const handleZoomIn = () => {
    setZoomLevel(zoomLevel + 0.4);
  };

  const handleZoomOut = () => {
    setZoomLevel(zoomLevel - 0.4);
    if (zoomLevel < 0.1) {
      setZoomLevel(0.1);
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>

      <div style={{ position: 'relative', width: '100%', height: '100%', maxWidth: '800px', maxHeight: '600px' }}>
      <div className="svg-container" ref={svgContainerRef} style={{ transform: `scale(${zoomLevel})`, width: '100%', height: '100%' }} />  
      </div>
      <div style={{ position: 'absolute', bottom: '10%', left: '50%', transform: 'translateX(-50%)'}}>
        <button onClick={handleZoomIn}>Zoom In</button>
        <button onClick={handleZoomOut}>Zoom Out</button>
      </div>
    </div>
  );
};

export default VizViewer;
