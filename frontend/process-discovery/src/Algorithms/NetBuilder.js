import { forceSimulation, forceLink, forceManyBody, forceCenter, forceX, forceY } from 'd3-force';

const assignPositions = (places, transitions, arcs, layoutType = 'hybrid', isVertical = true) => {
  if (!Array.isArray(places) || !Array.isArray(transitions) || !Array.isArray(arcs)) {
    console.error('Invalid input: places, transitions, and arcs must be arrays');
    return { places: [], transitions: [], arcs: [] };
  }

  const nodes = [...places, ...transitions];
  const edges = arcs.map(arc => ({
    source: nodes.find(node => node.id === arc.sourceId),
    target: nodes.find(node => node.id === arc.targetId)
  }));

  switch (layoutType) {
    case 'force-directed':
      applyForceDirectedLayout(nodes, edges);
      break;
    case 'hybrid':
      applyHybridLayout(nodes, edges, isVertical);
      break;
    case 'layered':
    default:
      applyLayeredLayout(nodes, edges, isVertical);
  }

  // Update original places and transitions with new positions
  nodes.forEach(node => {
    if (places.includes(node)) {
      const place = places.find(p => p.id === node.id);
      place.x = node.x;
      place.y = node.y;
    } else {
      const transition = transitions.find(t => t.id === node.id);
      transition.x = node.x;
      transition.y = node.y;
    }
  });

  return { places, transitions, arcs };
};

const applyLayeredLayout = (nodes, edges, isVertical) => {
  // Step 1: Cycle removal (assuming acyclic for simplicity)
  // Step 2: Layer assignment
  const layers = assignLayers(nodes, edges);
  
  // Step 3: Crossing reduction
  const orderedLayers = minimizeCrossings(layers, edges);
  
  // Step 4: Coordinate assignment
  assignCoordinates(orderedLayers, isVertical);

  // Step 5: Resource-based vertical layering
  applyResourceLayering(nodes);
};

const applyForceDirectedLayout = (nodes, edges) => {
  const simulation = forceSimulation(nodes)
    .force("link", forceLink(edges).id(d => d.id).distance(100))
    .force("charge", forceManyBody().strength(-1000))
    .force("center", forceCenter(300, 300))
    .stop();

  // Run the simulation synchronously
  for (let i = 0; i < 300; ++i) simulation.tick();
};

const applyHybridLayout = (nodes, edges, isVertical) => {
  // First apply layered layout
  applyLayeredLayout(nodes, edges, isVertical);

  // Then apply force-directed layout with initial positions from layered layout
  const simulation = forceSimulation(nodes)
    .force("link", forceLink(edges).id(d => d.id).distance(100))
    .force("charge", forceManyBody().strength(-500))
    .force("x", forceX(d => d.x).strength(0.1))
    .force("y", forceY(d => d.y).strength(0.1))
    .stop();

  // Run the simulation synchronously
  for (let i = 0; i < 100; ++i) simulation.tick();
};

const assignLayers = (nodes, edges) => {
  const layers = [];
  const visited = new Set();

  const dfs = (node, depth) => {
    if (visited.has(node)) return;
    visited.add(node);
    
    if (!layers[depth]) layers[depth] = [];
    layers[depth].push(node);

    const outgoingEdges = edges.filter(edge => edge.source === node);
    outgoingEdges.forEach(edge => dfs(edge.target, depth + 1));
  };

  nodes.forEach(node => {
    if (!visited.has(node)) dfs(node, 0);
  });
  console.log("LAYERS");
  console.log(layers);
  return layers;
};

const minimizeCrossings = (layers, edges) => {
  // Simple barycentric method
  for (let i = 1; i < layers.length; i++) {
    layers[i].sort((a, b) => {
      const aValue = edges.filter(e => e.target === a).reduce((sum, e) => sum + layers[i-1].indexOf(e.source), 0);
      const bValue = edges.filter(e => e.target === b).reduce((sum, e) => sum + layers[i-1].indexOf(e.source), 0);
      return aValue - bValue;
    });
  }
  return layers;
};

const assignCoordinates = (layers, isVertical) => {
  const layerSpacing = 100;
  const nodeSpacing = 50;
  layers.forEach((layer, layerIndex) => {
    const layerSize = layer.length * nodeSpacing;
    layer.forEach((node, nodeIndex) => {
      if (isVertical) {
        node.x = layerIndex * layerSpacing;
        node.y = (nodeIndex * nodeSpacing) + (nodeSpacing / 2);
      } else {
        node.x = (nodeIndex * nodeSpacing) + (nodeSpacing / 2);
        node.y = layerIndex * layerSpacing;
      }
    });
  });
};

const applyResourceLayering = (nodes) => {
  const resourceMap = new Map();
  
  // Group nodes by resource
  nodes.forEach(node => {
    if (!resourceMap.has(node.resource)) {
      resourceMap.set(node.resource, []);
    }
    resourceMap.get(node.resource).push(node);
  });

  // Assign vertical positions based on resource
  const resourceSpacing = 200;
  let currentY = 0;
  
  resourceMap.forEach((resourceNodes, resource) => {
    resourceNodes.forEach(node => {
      node.y += currentY;
    });
    currentY += resourceSpacing;
  });
};

export default assignPositions;