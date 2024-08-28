import { DOMParser } from 'xmldom';

export const parsePnml = (pnmlContent) => {
  try {
    console.log(pnmlContent);
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(pnmlContent, 'text/xml');
    console.log("doc arrived");

    console.log(xmlDoc);
    const net = xmlDoc.getElementsByTagName('net')[0];
    const places = Array.from(net.getElementsByTagName('place')).map(place => ({
      id: place.getAttribute('id'),
      name: place.getElementsByTagName('name')[0]?.getElementsByTagName('text')[0]?.textContent || place.getAttribute('id') || '',
      x: parseFloat(place.getElementsByTagName('graphics')[0]?.getElementsByTagName('position')[0]?.getAttribute('x') || '0'),
      y: parseFloat(place.getElementsByTagName('graphics')[0]?.getElementsByTagName('position')[0]?.getAttribute('y') || '0'),
    }));

    const transitions = Array.from(net.getElementsByTagName('transition')).map(transition => ({
      id: transition.getAttribute('id'),
      name: transition.getElementsByTagName('name')[0]?.getElementsByTagName('text')[0]?.textContent || transition.getAttribute('id') || '',
      x: parseFloat(transition.getElementsByTagName('graphics')[0]?.getElementsByTagName('position')[0]?.getAttribute('x') || '0'),
      y: parseFloat(transition.getElementsByTagName('graphics')[0]?.getElementsByTagName('position')[0]?.getAttribute('y') || '0'),
    }));

    const arcs = Array.from(net.getElementsByTagName('arc')).map(arc => ({
      id: arc.getAttribute('id'),
      sourceId: arc.getAttribute('source') || '',
      targetId: arc.getAttribute('target') || '',
    }));
    
    return { places, transitions, arcs };
  } catch (error) {
    console.error('Error parsing PNML:', error);
    return { places: [], transitions: [], arcs: [] };
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
      resource: place.resource
    }));

    const transitions = parsedJson.transitions.map(transition => ({
      id: transition.id,
      name: transition.label || transition.id,
      x: 0,  // We'll use the NetBuilder to assign positions
      y: 0,
      resource: transition.resource
    }));

    const arcs = parsedJson.arcs.map(arc => ({
      id: `${arc.source}_to_${arc.target}`,
      sourceId: arc.source,
      targetId: arc.target
    }));

    // Add initial and final markings to the places
    parsedJson.initialMarking.forEach(placeId => {
      const place = places.find(p => p.id === placeId);
      if (place) {
        place.tokens = (place.tokens || 0) + 1;
      }
    });

    parsedJson.finalMarking.forEach(placeId => {
      const place = places.find(p => p.id === placeId);
      if (place) {
        place.isFinal = true;
      }
    });

    return { places, transitions, arcs };
  } catch (error) {
    console.error('Error parsing JSON:', error);
    return { places: [], transitions: [], arcs: [] };
  }
};
