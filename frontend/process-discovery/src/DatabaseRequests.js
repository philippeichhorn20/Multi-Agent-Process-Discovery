/*

Type of request:
- run miner:
	- basic_split
	- basic_inductive
	--> Return PetriNet, FitnessMeasures
	- compositional_split
	- compositional_basic
	--> Return PetriNet, AbstractNet, abstractnetIsSound, FitnessMeasures
## in viewer: show small petri net in 

*/
import axios from 'axios'; // Import axios for API calls
import { parsePnmlToDot } from './Parser/dot_parser';

export async function run_miner(xes_file, miner_type, noise_threshold=0, use_compositional, alignement_metrics, entropy_metrics){
	if(xes_file && miner_type){
		const formData = new FormData();
		formData.append('file', xes_file);
		formData.append('algorithm', miner_type);
		formData.append("use_compositional", use_compositional)
		formData.append("alignment_metrics",alignement_metrics )
		formData.append("entropy_metrics", entropy_metrics)
		if (miner_type === 'inductive') {
		  formData.append('noise_threshold', noise_threshold);
		}
		try {
		  const response = await axios.post('http://localhost:8000/discover', formData, {
			headers: {
			  'Content-Type': 'multipart/form-data',
			},
			responseType: 'text', // Expecting PNML format
			timeout: 600000,
			withCredentials: true,
		  });
		  const jsonData = JSON.parse(response.data); // Parse the JSON string
		  const { dotString: parsedDotString, uniqueResources: resources, colors } = parsePnmlToDot(jsonData.net); // Parse PNML to DOT for net
		  const { dotString: abstractedDotString, uniqueResources: a, colors: ab } = parsePnmlToDot(jsonData.abstract_net, resources); // Parse PNML to DOT for abstract net

		  return {
			"dotstring": parsedDotString, 
			"stats": jsonData.stats,
			"abstractedDotString": abstractedDotString,
			"colors": colors,
			"resources": resources
		  }; // Return parsed data
		}catch (error) {
			console.error('Error during API call:', error);
		}	
}else{
	console.error("the given value were not the right types, should be: (File, String (ie miner o. split), [Number])", typeof(xes_file))
}
}




