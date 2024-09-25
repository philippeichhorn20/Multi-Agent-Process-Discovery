// import React, { useState, useEffect, useRef } from 'react';
// import { Graphviz } from '@hpcc-js/wasm/graphviz';
// import { TransformWrapper, TransformComponent } from 'react-zoom-pan-pinch';

// const GraphvizViewer = ({ dotString }) => {
//   const [svgString, setSvgString] = useState('');
//   const graphvizRef = useRef(null);

//   useEffect(() => {
//     const initializeGraphviz = async () => {
//       graphvizRef.current = await Graphviz.load();
//     };
//     initializeGraphviz();
//   }, []);

//   useEffect(() => {
//     if (graphvizRef.current && dotString) {
//       try {
//         const svg = graphvizRef.current.layout(dotString, 'svg', 'dot');
//         setSvgString(svg);
//       } catch (error) {
//         console.error('Error rendering graph:', error);
//       }
//     }
//   }, [dotString]);

//   return (
//     <div className="graphviz-viewer" style={{ maxWidth: '100%', maxHeight: '100%', overflow: 'auto' }}>
      
      
//       <TransformWrapper
//         initialScale={1}
//         initialPositionX={0}
//         initialPositionY={0}
//       >
//         <TransformComponent>
//           <div dangerouslySetInnerHTML={{ __html: svgString }} />
//         </TransformComponent>
//       </TransformWrapper>
//     </div>
//   );
// };

// export default GraphvizViewer;