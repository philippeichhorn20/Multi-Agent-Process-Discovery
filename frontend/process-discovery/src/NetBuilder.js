const assignPositions = (places, transitions, arcs) => {
  // Check if places, transitions, and arcs are defined and are arrays
  if (!Array.isArray(places) || !Array.isArray(transitions) || !Array.isArray(arcs)) {
    console.error('Invalid input: places, transitions, and arcs must be arrays');
    return { places: [], transitions: [], arcs: [] };
  }

  const startPlaces = places.filter(place => !arcs.some(arc => arc.targetId === place.id));
  const visited = new Set();
  const levelMap = new Map();
  const elementWidth = 80;
  const elementHeight = 80;

  const assignPositionsRecursive = (elementId, level = 0, verticalPosition = 0) => {
    if (visited.has(elementId)) return verticalPosition;
    visited.add(elementId);

    const element = [...places, ...transitions].find(el => el.id === elementId);
    if (!element) return verticalPosition;

    element.x = level * elementWidth;
    element.y = verticalPosition;

    levelMap.set(elementId, level);

    const outgoingArcs = arcs.filter(arc => arc.sourceId === elementId);
    let nextVerticalPosition = verticalPosition;

    outgoingArcs.forEach((arc, index) => {
      const yOffset = index * (elementHeight / 2);
      nextVerticalPosition = assignPositionsRecursive(arc.targetId, level + 1, verticalPosition + yOffset);
    });

    return Math.max(verticalPosition, nextVerticalPosition);
  };

  let verticalPosition = 0;
  startPlaces.forEach(place => {
    verticalPosition = assignPositionsRecursive(place.id, 0, verticalPosition);
  });

  // Handle any disconnected elements
  [...places, ...transitions].forEach(element => {
    if (!visited.has(element.id)) {
      assignPositionsRecursive(element.id, 0, verticalPosition);
      verticalPosition += elementHeight;
    }
  });

  // Sort elements by their assigned positions
  const sortByPosition = (elements) => {
    return elements.sort((a, b) => {
      if (a.x !== b.x) return a.x - b.x;
      return a.y - b.y;
    });
  };

  const sortedPlaces = sortByPosition(places);
  const sortedTransitions = sortByPosition(transitions);
  console.log(sortedPlaces);
  console.log(sortedTransitions);
  console.log(arcs);
  return { 
    places: sortedPlaces, 
    transitions: sortedTransitions,
    arcs: arcs 
  };
};

export default assignPositions;