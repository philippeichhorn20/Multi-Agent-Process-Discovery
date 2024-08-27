import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';
import assignPositions from './NetBuilder';

const NetViewer = ({ netElements }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current || !netElements) return;

    console.log('NetElements:', netElements);  // Debug log

    const { places, transitions, arcs } = assignPositions(
      netElements.places,
      netElements.transitions,
      netElements.arcs
    );
    

    console.log('Assigned positions:', { places, transitions, arcs });  // Debug log

    const elements = [
      // Nodes (places and transitions)
      ...places.map(place => {
        if (!place.id) console.log('Place with no ID:', place);  // Debug warning
        return {
          data: { id: place.id || `place_${Math.random()}`, label: place.tokens > 0 ? place.tokens.toString() : '' },
          position: { x: place.x, y: place.y },
          classes: ['place']
        };
      }),
      ...transitions.map(transition => {
        if (!transition.id) console.log('Transition with no ID:', transition);  // Debug warning
        return {
          data: { id: transition.id || `transition_${Math.random()}` },
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
            'text-halign': 'center'
          }
        },
        {
          selector: '.place',
          style: {
            'shape': 'ellipse',
            'width': 30,
            'height': 30,
            'background-color': '#fff',
            'border-width': 2,
            'border-color': '#000'
          }
        },
        {
          selector: '.transition',
          style: {
            'shape': 'rectangle',
            'width': 30,
            'height': 20,
            'background-color': '#000'
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

    cy.fit();
    cy.center();

    return () => {
      cy.destroy();
    };
  }, [netElements]);

  return <div ref={containerRef} style={{ width: '100%', height: '100%', textAlign: 'left' }} />;
};

export default React.memo(NetViewer);