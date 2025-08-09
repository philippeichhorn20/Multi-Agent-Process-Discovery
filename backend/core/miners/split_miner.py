from services.log_store import LogStore
import logging
from pm4py import convert_to_petri_net, read_bpmn
import subprocess

async def run_split_miner_basic(log_storage: LogStore, noise_threshold):
    print(f"Basic: Starting Split Miner basic with noise threshold {noise_threshold}")
    try:
        if not noise_threshold:
            noise_threshold = 0
        net, im, fm = split_miner(log_storage.xes_path, noise_threshold)
        return net, im, fm 
    except Exception as e:
        logging.error(f"Error during discovery, split: {str(e)}")
        raise


def split_miner(path: str, var):
	output_path = "/Users/philippeichhorn/IdeaProjects/Multi-Agent-Process-Discovery/backend/output"
	cmd = ["java", "-cp", f"split-miner-2/sm2.jar:split-miner-2/lib/*", "au.edu.unimelb.services.ServiceProvider", "SM2", path, output_path, f"{var}"]
	result = subprocess.run(cmd)
	bpmn  = read_bpmn(f'{output_path}.bpmn')
	petri_net = convert_to_petri_net(bpmn)
	net, im, fm = petri_net
	return net, im, fm
