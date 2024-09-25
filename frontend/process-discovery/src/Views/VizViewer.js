import React, { useEffect, useRef, useState } from 'react';
import { instance } from "@viz-js/viz";
import { TransformWrapper, TransformComponent } from 'react-zoom-pan-pinch';


const VizViewer = ({ dotString, width, height, setDotString }) => {
  const [svg, setSvg] = useState(null);
  const vizRef = useRef(null);
  const svgContainerRef = useRef(null);
  const [dotstring, setDotstring] = useState(dotString)
  const [zoomLevel, setZoomLevel] = useState(1);

  const renderGraph = async (viz) => {
    if (viz && dotstring) {
      try {
        const svgElement = await viz.renderSVGElement(dotstring);
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
  const downloadSvg = () => {
    if (svg) {
      const svgData = new XMLSerializer().serializeToString(svg);
      const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
      const svgUrl = URL.createObjectURL(svgBlob);
      const downloadLink = document.createElement('a');
      downloadLink.href = svgUrl;
      downloadLink.download = 'graph.svg'; // Name of the downloaded file
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    }
  };

  useEffect(() => {
    instance().then(viz => {
      vizRef.current = viz;
      renderGraph(viz); // Call renderGraph with the viz instance
    });
  }, []);

  useEffect(() => {
    if (vizRef.current) {
      renderGraph(vizRef.current); // Re-render graph when dotstring changes
    }
  }, [dotstring]);

  const changeDirection = () =>{
  let newDotString = ""
    if (dotstring.includes("rankdir=LR")){
      newDotString = dotstring.replace("rankdir=LR", "rankdir=TD")
    }else{
      newDotString = dotstring.replace("rankdir=TD", "rankdir=LR")
    }
    setDotstring(newDotString)
    renderGraph(vizRef.current)
  }

  return (
    <div className="graphviz-viewer" style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <button onClick={downloadSvg} style={{ position: "absolute", bottom:0, right:0, zIndex:10, margin:10
       }}>
        Download SVG
      </button>
      <button onClick={changeDirection} style={{ position: "absolute", bottom:0, left:0, zIndex:10, margin:10
       }}>
        switcheroo
      </button>
      <TransformWrapper
        initialScale={1}
        initialPositionX={0}
        initialPositionY={0}
        
      >
        <TransformComponent>
        <div className="svg-container" ref={svgContainerRef} style={{ width: width, height: height}} />  
        </TransformComponent>
      </TransformWrapper>

    </div>
  );
};

export default VizViewer;
