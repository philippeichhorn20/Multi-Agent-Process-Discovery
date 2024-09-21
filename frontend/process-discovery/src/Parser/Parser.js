import { DOMParser } from 'xmldom';

export const parsePnml = (pnmlContent) => {
  try {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(pnmlContent, 'text/xml');
    console.log("doc arrived");

    const net = xmlDoc.getElementsByTagName('net')[0];
    const places = Array.from(net.getElementsByTagName('place')).map(place => ({
      id: place.getAttribute('id'),
      name: place.getElementsByTagName('name')[0]?.getElementsByTagName('text')[0]?.textContent || place.getAttribute('id') || '',
      x: parseFloat(place.getElementsByTagName('graphics')[0]?.getElementsByTagName('position')[0]?.getAttribute('x') || '0'),
      y: parseFloat(place.getElementsByTagName('graphics')[0]?.getElementsByTagName('position')[0]?.getAttribute('y') || '0'),
      resource: place.getAttribute('resource') || '',
    }));

    const transitions = Array.from(net.getElementsByTagName('transition')).map(transition => ({
      id: transition.getAttribute('id'),
      name: transition.getElementsByTagName('name')[0]?.getElementsByTagName('text')[0]?.textContent || transition.getAttribute('id') || '',
      x: parseFloat(transition.getElementsByTagName('graphics')[0]?.getElementsByTagName('position')[0]?.getAttribute('x') || '0'),
      y: parseFloat(transition.getElementsByTagName('graphics')[0]?.getElementsByTagName('position')[0]?.getAttribute('y') || '0'),
      label: transition.getAttribute('label') || '',
      resource: transition.getAttribute('resource') || '',
    }));

    const arcs = Array.from(net.getElementsByTagName('arc')).map(arc => ({
      id: arc.getAttribute('id'),
      sourceId: arc.getAttribute('source') || '',
      targetId: arc.getAttribute('target') || '',
    }));

    const initialMarking = {};
    const finalMarking = {};
    Array.from(net.getElementsByTagName('place')).forEach(place => {
      const initialMarkingElement = place.getElementsByTagName('initialMarking')[0];
      const finalMarkingElement = place.getElementsByTagName('finalMarking')[0];
      if (initialMarkingElement) {
        initialMarking[place.getAttribute('id')] = parseInt(initialMarkingElement.getElementsByTagName('text')[0]?.textContent || '0');
      }
      if (finalMarkingElement) {
        finalMarking[place.getAttribute('id')] = parseInt(finalMarkingElement.getElementsByTagName('text')[0]?.textContent || '0');
      }
    });
    
    return { places, transitions, arcs, initialMarking, finalMarking };
  } catch (error) {
    console.error('Error parsing PNML:', error);
    return { places: [], transitions: [], arcs: [], initialMarking: {}, finalMarking: {} };
  }
};

export const parseJson = (jsonContent) => {
  try {
    console.log(jsonContent);
    const parsedJson = JSON.parse(jsonContent);
    console.log("JSON parsed successfully");

    const places = parsedJson.places.map(place => ({
      id: place.id,
      name: place.id,
      x: 0,  // We'll use the NetBuilder to assign positions
      y: 0,
      resource: place.resource || '',
    }));

    const transitions = parsedJson.transitions.map(transition => ({
      id: transition.id,
      name: transition.id,
      label: transition.label,
      x: 0,  // We'll use the NetBuilder to assign positions
      y: 0,
      resource: transition.resource || '',
    }));

    const arcs = parsedJson.arcs.map(arc => ({
      id: `${arc.source}_to_${arc.target}`,
      sourceId: arc.source,
      targetId: arc.target,
    }));

    // Parse initial marking
    const initialMarking = {};
    parsedJson.initialMarking.forEach(placeId => {
      initialMarking[placeId] = (initialMarking[placeId] || 0) + 1;
    });

    // Parse final marking
    const finalMarking = {};
    parsedJson.finalMarking.forEach(placeId => {
      finalMarking[placeId] = (finalMarking[placeId] || 0) + 1;
    });

    return { 
      places, 
      transitions, 
      arcs, 
      initialMarking, 
      finalMarking,
    };
  } catch (error) {
    console.error('Error parsing JSON:', error);
    return { 
      places: [], 
      transitions: [], 
      arcs: [], 
      initialMarking: {}, 
      finalMarking: {},
    };
  }
};
