from pandas import DataFrame
from pm4py import discover_petri_net_inductive
import pm4py
import subprocess


def split_miner(path: str, var):
	output_path = "/Users/philippeichhorn/IdeaProjects/Multi-Agent-Process-Discovery/backend/output"
	cmd = ["java", "-cp", f"split-miner-2/sm2.jar:split-miner-2/lib/*", "au.edu.unimelb.services.ServiceProvider", "SM2", path, output_path, f"{var}"]
	result = subprocess.run(cmd)
	bpmn  = pm4py.read_bpmn(f'{output_path}.bpmn')
	petri_net = pm4py.convert_to_petri_net(bpmn)
	net, im, fm = petri_net
	return net, im, fm
