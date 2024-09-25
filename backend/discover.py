import pm4py
import logging
import os
import asyncio
import json
import pm4py.objects.petri_net.utils as pnutils
from InteractionUtils import InteractionUtils
from miner_algorithms import split_miner
from NetStorer import NetStorer
from data_loader import Data_Loader
from itertools import chain
from Reducer import Reducer
import pandas as pd
# Configure logging


async def run_inductive_miner_basic(net_storage: NetStorer, noise_threshold):
    print(f"BAsic: Starting Inductive Miner basic with noise threshold {noise_threshold}")
    try:
        if not noise_threshold:
            noise_threshold = 0
        net, im, fm = pm4py.discover_petri_net_inductive(net_storage.df, noise_threshold=noise_threshold)

    except Exception as e:
        logging.error(f"Error during discoveryn inductive: {str(e)}")
        raise
    return net, im, fm



async def run_split_miner_basic(net_storage: NetStorer, noise_threshold):
    print(f"BAsic: Starting Split Miner basic with noise threshold {noise_threshold}")
    try:
        if not noise_threshold:
            noise_threshold = 0
        net, im, fm = split_miner(net_storage.xes_path, noise_threshold)
        return net, im, fm 
    except Exception as e:
        logging.error(f"Error during discovery, split: {str(e)}")
        raise


async def run_miner_compose(net_storage, noise_threshold, miner):

    df_grouped = Data_Loader.group_dataframe_by_resource(net_storage)
    nets = []
    # Merge the discovered Petri nets
    if miner == "split":
        temp_path = "temp_split_single_resource.xes"
        for name, group in df_grouped:

            print(type(group))
            try:
            # Write the grouped data to a temp file
                print("prepre splitr")
                
                pm4py.write.write_xes(log=group, file_path=temp_path)
                print("pre splitr")

                if not noise_threshold:
                    noise_threshold = 0

                net, im, fm = split_miner(path=temp_path, var=noise_threshold)
                print("post splitr")

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
            net, im, fm  = pm4py.discover_petri_net_inductive(group, noise_threshold= noise_threshold)
            for x in net.places:
                x.properties.update({"resource": name})
            for x in net.transitions:
                x.properties.update({"resource": name})
            nets.append((net, im, fm))

    
    abstracted_nets = Reducer.apply_all(nets)
    abstracted_net, im_abstract, fm_abstract = InteractionUtils.merge_two_nets(abstracted_nets)

    merged_net, im, fm = InteractionUtils.merge_two_nets(nets)

    return merged_net, im, fm, abstracted_net, im_abstract, fm_abstract 



async def run_split_miner_compose(file_content):
    temp_file_path = 'temp_log.xes'
    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(file_content)
    log = await asyncio.to_thread(pm4py.read_xes, temp_file_path)
    
    # Convert log to dataframe and group by org:resource
    df = pm4py.convert_to_dataframe(log)
    df_grouped = df.groupby('org:resource')
    
    nets = []
    for name, group in df_grouped:
        net, im, fm = await asyncio.to_thread(pm4py.discover_petri_net_split_miner, group)
        # Add resource name to places and transitions
        for place in net.places:
            place.properties['resource'] = name
        for transition in net.transitions:
            transition.properties['resource'] = name
        nets.append((net, im, fm, name))
    
    # Merge the discovered Petri nets
    merged_net, merged_im, merged_fm = pnutils.petri_utils.merge([n[0] for n in nets])
    
    return await asyncio.to_thread(export_to_json, merged_net, merged_im, merged_fm)


def export_to_pnml(net, initial_marking, final_marking):
    logging.info("Exporting Petri net to PNML")
    temp_pnml_path = 'final_output.pnml'
    try:
        pm4py.write_pnml(net, initial_marking, final_marking, temp_pnml_path)
        with open(temp_pnml_path, 'r') as pnml_file:
            pnml_content = pnml_file.read()
        return pnml_content
    except Exception as e:
        logging.error(f"Error during PNML export: {str(e)}")
        raise
    finally:
        if os.path.exists(temp_pnml_path):
            os.remove(temp_pnml_path)

def export_to_json(net, initial_marking, final_marking):
    logging.info("Exporting Petri net to JSON")

    places = [{"id": place.name, "resource": place.properties.get('resource', '')} for place in net.places]
    transitions = [{"id": trans.name, "label": trans.label, "resource": trans.properties.get('resource', '')} for trans in net.transitions]
    arcs = [{"source": arc.source.name, "source.resource": arc.source.properties.get('resource', ''), "target": arc.target.name, "target.resource": arc.target.properties.get('resource', '')} for arc in net.arcs]

    initial_marking_places = [place.name for place, count in initial_marking.items() for _ in range(count)]
    final_marking_places = [place.name for place, count in final_marking.items() for _ in range(count)]

    petri_net_json = {
        "places": places,
        "transitions": transitions,
        "arcs": arcs,
        "initialMarking": initial_marking_places,
        "finalMarking": final_marking_places
    }
    return json.dumps(petri_net_json)