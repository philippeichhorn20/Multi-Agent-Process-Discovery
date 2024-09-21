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

export async function basic_miner(xes_file, miner_type, noise_threshold=0){
	if(xes_file && miner_type){
		const formData = new FormData();
		formData.append('file', xes_file);
		formData.append('algorithm', miner_type);
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
		  const parsedDotString = parsePnmlToDot(jsonData.net); // Parse PNML to DOT
		  return {
			"dotstring": parsedDotString, 
			"stats":jsonData.stats
		  }; // Return parsed data
		}catch (error) {
			console.error('Error during API call:', error);
		}	
}else{
	console.error("the given value were not the right types, should be: (File, String (ie miner o. split), [Number])", typeof(xes_file))
}
}




