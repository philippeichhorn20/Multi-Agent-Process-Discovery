import { DOMParser } from 'xmldom';

export const parsePnmlToDot = (pnmlContent, args) => {
  try {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(pnmlContent, 'text/xml');
    const net = xmlDoc.getElementsByTagName("net")[0];
    let dotString = 'digraph PetriNet {\n';
    dotString += '  rankdir=LR;\n';
    dotString += '  node [shape=circle];\n';
    dotString += '  node [shape=box];\n\n';
    const colors = ['red', 'blue', 'green', 'grey', 'orange', 'pink'];
    console.log(pnmlContent)
    let uniqueResources = args
    if (!args){
      uniqueResources = new Set();
      Array.from(net.getElementsByTagName('place')).forEach(place => {
        const name = place.getElementsByTagName('name')[0]?.getElementsByTagName('text')[0]?.textContent || place.getAttribute('id');
        if (name && name != "") {
          const firstPart = name.split(':')[0].trim();
          if (firstPart) {
            uniqueResources.add(firstPart);
          }
        }
      });
  
      uniqueResources = Array.from(uniqueResources);
    }


    
    // Parse places
    Array.from(net.getElementsByTagName('place')).forEach(place => {
      const id = place.getAttribute('id');
      const name = place.getElementsByTagName('name')[0]?.getElementsByTagName('text')[0]?.textContent || id;
      if (id) {
        //label="${name.split(':')[1].trim()}"
        dotString += `  "${id}" [label= "" shape=circle, color="${colors[uniqueResources.indexOf(name.split(':')[0].trim())%uniqueResources.length]}"];\n`;
      }
    });

    // Parse transitions
    Array.from(net.getElementsByTagName('transition')).forEach(transition => {
      const id = transition.getAttribute('id');
      const name = transition.getElementsByTagName('name')[0]?.getElementsByTagName('text')[0]?.textContent || id;
      if (id) {
        dotString += `  "${id}" [label="${name.split(':')[1].trim()}", shape=box, color="${colors[uniqueResources.indexOf(name.split(':')[0].trim())%uniqueResources.length]}"];\n`;
      }
    });
    console.log(dotString)

    // Parse arcs
    Array.from(net.getElementsByTagName('arc')).forEach(arc => {
      const source = arc.getAttribute('source');
      const target = arc.getAttribute('target');
      dotString += `  "${source}" -> "${target}";\n`;
    });

    dotString += '}\n';
    dotString = dotString.replace(/:/g, "__");
    return {dotString, uniqueResources, colors};
  } catch (error) {
    console.error('Error parsing PNML to DOT:', error);
    return ('', new Set(), new Set());
  }
};

export const parseJsonToDot = (jsonContent) => {
  try {
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
    return removeDuplicateRows(dotString);
  } catch (error) {
    console.error('Error parsing JSON to DOT:', error);
    return '';
  }
};


function removeDuplicateRows(str) {
  // Split the string into an array of rows
  const rows = str.split('\n');
  
  // Use a Set to filter out duplicates
  const uniqueRows = [...new Set(rows)];
  
  // Join the unique rows back into a string
  return uniqueRows.join('\n');
}