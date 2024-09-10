import { DOMParser } from 'xmldom';

export const parsePnmlToDot = (pnmlContent) => {
  try {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(pnmlContent, 'text/xml');
    const net = xmlDoc.getElementsByTagName('net')[0];

    let dotString = 'digraph PetriNet {\n';
    dotString += '  rankdir=LR;\n';
    dotString += '  node [shape=circle];\n';
    dotString += '  node [shape=box];\n\n';


    // Parse places
    Array.from(net.getElementsByTagName('place')).forEach(place => {
      const id = place.getAttribute('id');
      const name = place.getElementsByTagName('name')[0]?.getElementsByTagName('text')[0]?.textContent || id;
      if (id) {
        dotString += `  "${id}" [label="${name}", shape=circle];\n`;
        console.log('places', id, name);
      }
    });

    // Parse transitions
    Array.from(net.getElementsByTagName('transition')).forEach(transition => {
      const id = transition.getAttribute('id');
      const name = transition.getElementsByTagName('name')[0]?.getElementsByTagName('text')[0]?.textContent || id;
      if (id) {
        dotString += `  "${id}" [label="${name}", shape=box];\n`;
        console.log('trasn', id, name);
      }
    });

    // Parse arcs
    Array.from(net.getElementsByTagName('arc')).forEach(arc => {
      const source = arc.getAttribute('source');
      const target = arc.getAttribute('target');
      dotString += `  "${source}" -> "${target}";\n`;
    });

    dotString += '}\n';
    return dotString;
  } catch (error) {
    console.error('Error parsing PNML to DOT:', error);
    return '';
  }
};

export const parseJsonToDot = (jsonContent) => {
  try {
    console.log(jsonContent)

    const parsedJson = JSON.parse(jsonContent);

    let dotString = 'digraph PetriNet {\n';
    dotString += '  rankdir=LR;\n';
    dotString += '  node [shape=circle];\n';
    dotString += '  node [shape=box];\n\n';
    // Parse places
    parsedJson.places.forEach(place => {
      dotString += `  "${place.id}" [label="${place.id}", shape=circle];\n`;
    });

    // Parse transitions
    parsedJson.transitions.forEach(transition => {
      dotString += `  "${transition.id}" [label="${transition.label}", shape=box];\n`;
    });

    // Parse arcs
    parsedJson.arcs.forEach(arc => {
      dotString += `  "${arc.source}" -> "${arc.target}";\n`;
    });

    dotString += '}\n';
    return dotString;
  } catch (error) {
    console.error('Error parsing JSON to DOT:', error);
    return '';
  }
};
