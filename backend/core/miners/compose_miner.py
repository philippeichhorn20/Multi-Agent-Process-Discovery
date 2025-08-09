import os
from pm4py.write import write_xes
from pm4py import discover_petri_net_inductive

from core.miners.interaction_utils import InteractionUtils
from .split_miner import split_miner
from services.data_loader import Data_Loader
from itertools import chain
from core.reducer import Reducer


async def run_miner_compose(log_storage, noise_threshold, miner):

    df_grouped = Data_Loader.group_dataframe_by_resource(log_storage)
    nets = []
    # Merge the discovered Petri nets
    if miner == "split":
        temp_path = "temp_split_single_resource.xes"
        for name, group in df_grouped:

            try:
            # Write the grouped data to a temp file
                
                write_xes(log=group, file_path=temp_path)

                if not noise_threshold:
                    noise_threshold = 0

                net, im, fm = split_miner(path=temp_path, var=noise_threshold)

                for x in chain(net.places, net.transitions):
                    x.properties.update({"resource": name})
                nets.append((net, im, fm))

            finally:
                # Delete the temp file after usage
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    else:
        for name, group in df_grouped:
            if not noise_threshold:
                noise_threshold = 0            
            net, im, fm  = discover_petri_net_inductive(group, noise_threshold= noise_threshold)
            for x in net.places:
                x.properties.update({"resource": name})
            for x in net.transitions:
                x.properties.update({"resource": name})
            nets.append((net, im, fm))

    
    abstracted_nets = Reducer.apply_all(nets)
    abstracted_net, im_abstract, fm_abstract = InteractionUtils.merge_two_nets(abstracted_nets)

    merged_net, im, fm = InteractionUtils.merge_two_nets(nets)

    return merged_net, im, fm, abstracted_net, im_abstract, fm_abstract 
