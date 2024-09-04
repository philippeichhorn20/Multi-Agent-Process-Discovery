import React, { useEffect, useRef, useState } from 'react';
import { instance } from "@viz-js/viz";

const VizViewer = ({ dotString, updateDotString }) => {
  const [svg, setSvg] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const vizRef = useRef(null);

  useEffect(() => {
    instance().then(viz => {
      vizRef.current = viz;
    });
  }, []);

  useEffect(() => {
    const renderGraph = async () => {
      if (vizRef.current && dotString) {
        setLoading(true);
        setError(null);
        try {
          const svgElement = await vizRef.current.renderSVGElement(dotString);
          console.log('SVG generated:', svgElement); // Debug log
          setSvg(svgElement);
        } catch (error) {
          console.error('Error rendering graph:', error);
          setError('Failed to render graph. Please check your DOT string.');
        } finally {
          setLoading(false);
        }
      }
    };
    renderGraph();
  }, [dotString]);

  console.log('Current dotString:', dotString); // Debug log

  return (
    <div className="viz-viewer">
      {loading && <p>Loading graph...</p>}
      {error && <p className="error">{error}</p>}
      {svg && <div ref={el => el && el.appendChild(svg)} />}
      {!svg && !loading && !error && <p>No graph to display. Please provide a valid DOT string.</p>}
      <div className="dot-string-display">
        <h3>DOT String:</h3>
        <pre>{dotString}</pre>
      </div>
    </div>
  );
};

export default VizViewer;
