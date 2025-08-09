
import axios from 'axios'; // Import axios for API calls
import { parsePnmlToDot } from './Parser/dot_parser';

let cancelTokenSource;

export async function run_miner(xes_file, miner_type, noise_threshold=0, use_compositional, alignement_metrics, entropy_metrics){
	if(xes_file && miner_type){
		const formData = new FormData();
		formData.append('file', xes_file);
		formData.append('algorithm', miner_type);
		formData.append("use_compositional", use_compositional)
		formData.append("alignment_metrics",alignement_metrics )
		formData.append("entropy_metrics", entropy_metrics)
		if (miner_type === 'inductive' && noise_threshold) {
		  	formData.append('noise_threshold', noise_threshold);
		}else{
			formData.append('noise_threshold', 0);
		}

		// Create a new CancelToken source
		cancelTokenSource = axios.CancelToken.source();

		try {
		  const response = await axios.post('http://localhost:8000/discover', formData, {
			headers: {
			  'Content-Type': 'multipart/form-data',
			},
			responseType: 'text', // Expecting PNML format
			timeout: 600000,
			withCredentials: true,
			cancelToken: cancelTokenSource.token, // Attach the cancel token to the request
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
			if (axios.isCancel(error)) {
				console.log('Request canceled', error.message);
				return "Request was canceled";
			} else {
				if (error.response) {
					console.error("Server responded with an error:", error.response.status);
					console.error("Error response data:", error.response.data); // This might contain useful info
					console.error("Error response headers:", error.response.headers);
				  } else if (error.request) {
					console.error("No response received. Error request details:", error.request);
				  } else {
					console.error("Error setting up request:", error.message);
				  }
				  console.error("Full error object:", error);
			}
		}	
	}else{
		console.error("the given value were not the right types, should be: (File, String (ie miner o. split), [Number])", typeof(xes_file));
		return "the given value were not the right types, should be: (File, String (ie miner o. split), [Number])";
	}
}

// Function to cancel the API call
export function cancelRunMiner() {
	console.log("cancel miner")
	if (cancelTokenSource) {
		cancelTokenSource.cancel('Operation canceled by the user.');
	}
}




