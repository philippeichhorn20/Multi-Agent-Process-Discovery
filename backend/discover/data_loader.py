import pm4py
import pandas as pd 


class Data_Loader:

    def create_petri_nets(path):
        log = pm4py.read_xes(file_path=path) 
        df = pm4py.convert_to_dataframe(log)
        df_grouped = df.groupby('org:resource')    # groups it by agent, in this dataset called "org:resource"     
        list_of_nets = []
        for name, group in df_grouped:
            # using Inductive Miner to discover a petri net of each agent seperately
            net, im, fm = pm4py.discover_petri_net_inductive(df, activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')
            list_of_nets.append((net, im, fm))
        return list_of_nets


    # Sample usage
    num = 1
    path = f'/Users/philippeichhorn/Downloads/Compositional process discovery_experiment data/IP-{num}/IP-{num}_initial_log.xes'
    list_of_nets = create_petri_nets(path)
    for net in list_of_nets:
        pnet, start, end = net
        pm4py.view_petri_net(pnet, start, end, format="svg")


