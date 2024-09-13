from pandas import DataFrame
from pm4py import discover_petri_net_inductive
import pm4py

def inductive_miner(path: str, noise_threshold=0):
	log = pm4py.read_xes(file_path=path)
	df = pm4py.convert_to_dataframe(log)
	net, im, fm = discover_petri_net_inductive(df, noise_threshold=noise_threshold)
	return net

def split_miner(path: str):
	jar_path = 

	net, im, fm = pm4py.objects.conversion.bpmn.variants.to_petri_net.apply(bpmn_graph=bpmn)

	