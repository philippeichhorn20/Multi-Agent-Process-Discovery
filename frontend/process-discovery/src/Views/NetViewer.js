import React, { useEffect, useRef, useState } from 'react';
import cytoscape from 'cytoscape';
import assignPositions from '../Algorithms/NetBuilder';
import './Views.css';

const NetViewer = ({ netElements }) => {
  const containerRef = useRef(null);
  const [layoutType, setLayoutType] = useState('hybrid');
  const [isVertical, setIsVertical] = useState(true);

  useEffect(() => {
    if (!containerRef.current || !netElements) return;

    console.log('NetElements:', netElements);  // Debug log

    const { places, transitions, arcs } = assignPositions(
      netElements.places,
      netElements.transitions,
      netElements.arcs,
      layoutType,
      isVertical
    );

    // Generate a color map for different resources
    const resourceColors = {};
    const getColorForResource = (resource) => {
      if (!resourceColors[resource]) {
        resourceColors[resource] = `#${Math.floor(Math.random()*16777215).toString(16)}`;
      }
      return resourceColors[resource];
    };

    const elements = [
      // Nodes (places and transitions)
      ...places.map(place => {
        if (!place.id) console.log('Place with no ID:', place);  // Debug warning
        return {
          data: { 
            id: place.id || `place_${Math.random()}`, 
            label: place.name || place.id,
            tokens: place.tokens > 0 ? place.tokens.toString() : '',
            resource: place.resource,
            name: place.name || place.id
          },
          position: { x: place.x, y: place.y },
          classes: ['place']
        };
      }),
      ...transitions.map(transition => {
        if (!transition.id) console.log('Transition with no ID:', transition);  // Debug warning
        return {
          data: { 
            id: transition.id || `transition_${Math.random()}`,
            label: transition.label || transition.id,
            resource: transition.resource,
            name: transition.name || transition.id
          },
          position: { x: transition.x, y: transition.y },
          classes: ['transition']
        };
      }),
      // Edges (arcs)
      ...(arcs || []).map(arc => {
        if (!arc.id || !arc.sourceId || !arc.targetId) console.log('Arc with missing data:', arc);  // Debug warning
        return {
          data: { 
            id: arc.id || `arc_${Math.random()}`,
            source: arc.sourceId || `source_${Math.random()}`, 
            target: arc.targetId || `target_${Math.random()}`
          }
        };
      })
    ];

    console.log('Cytoscape elements:', elements);  // Debug log

    const cy = cytoscape({
      container: containerRef.current,
      elements: elements,
      style: [
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'text-valign': 'center',
            'text-halign': 'center',
            'text-wrap': 'wrap',
            'text-max-width': '100px'
          }
        },
        {
          selector: '.place',
          style: {
            'shape': 'ellipse',
            'width': 40,
            'height': 40,
            'background-color': 'data(resource)',
            'border-width': 2,
            'border-color': '#000',
            'text-margin-y': -5
          }
        },
        {
          selector: '.place[?tokens]',
          style: {
            'label': function(ele) {
              return ele.data('label') + '\n' + ele.data('tokens');
            }
          }
        },
        {
          selector: '.transition',
          style: {
            'shape': 'rectangle',
            'width': 40,
            'height': 30,
            'background-color': 'data(resource)'
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': '#000',
            'target-arrow-color': '#000',
            'target-arrow-shape': 'triangle',
            'source-endpoint': 'outside-to-node-or-label',
            'target-endpoint': 'outside-to-node-or-label',
            'curve-style': 'bezier',
            'control-point-step-size': 40
          }
        }
      ],
      layout: {
        name: 'preset'
      }
    });

    // Apply colors based on resource
    cy.nodes().forEach(node => {
      const resource = node.data('resource');
      if (resource) {
        node.style('background-color', getColorForResource(resource));
      }
    });

    // Add click event to show name and all properties
    cy.on('tap', 'node, edge', function(evt){
      const element = evt.target;
      const data = element.data();
      let message = `Name: ${data.name || 'N/A'}\n\nAll Properties:\n`;
      for (let [key, value] of Object.entries(data)) {
        message += `${key}: ${value}\n`;
      }
      alert(message);
    });

    cy.fit();
    cy.center();

    return () => {
      cy.destroy();
    };
  }, [netElements, layoutType, isVertical]);

  return (
    <div className="net-viewer-container">
      <div ref={containerRef} className="net-viewer" />
      <div className="layout-controls">
        <select value={layoutType} onChange={(e) => setLayoutType(e.target.value)}>
          <option value="force-directed">Force Directed</option>
          <option value="hybrid">Hybrid</option>
          <option value="layered">Layered</option>
          <option value="graphviz-style">graphviz-style</option>
        </select>
        <label>
          <input
            type="checkbox"
            checked={isVertical}
            onChange={(e) => setIsVertical(e.target.checked)}
          />
          Vertical Layout
        </label>
      </div>
    </div>
  );
};

export default React.memo(NetViewer);