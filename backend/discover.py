import pm4py
import logging
import os
import asyncio
import json
import pm4py.objects.petri_net.utils as pnutils
from InteractionUtils import InteractionUtils

# Configure logging

async def run_inductive_miner(file_content, noise_threshold):
    logging.info(f"Starting Inductive Miner discovery with noise threshold {noise_threshold}")
    temp_file_path = 'temp_log.xes'
    try:
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(file_content)
        log = pm4py.read_xes(temp_file_path)
        # Convert log to dataframe and group by org:resource
        df = pm4py.convert_to_dataframe(log)
        df_grouped = df.groupby('org:resource')

        nets = []

        for name, group in df_grouped:
            net, im, fm = pm4py.discover_petri_net_inductive(group, noise_threshold=noise_threshold)

            # Add resource name to places and transitions
            for place in net.places:
                place.properties['resource'] = name
            for transition in net.transitions:
                transition.properties['resource'] = name
            nets.append((net, im, fm))
        # Merge the discovered Petri nets
       
        merged_net = InteractionUtils.merge_two_nets([net[0] for net in nets][0], [net[0] for net in nets][1])

        logging.info("Discovery and merging completed successfully")
        return await asyncio.to_thread(export_to_json, merged_net, nets[0][1], nets[0][2])
    except Exception as e:
        logging.error(f"Error during discovery: {str(e)}")
        raise
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        logging.info("Temporary file removed")


def export_to_pnml(net, initial_marking, final_marking):
    logging.info("Exporting Petri net to PNML")
    temp_pnml_path = 'temp_net.pnml'
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
        logging.info("Temporary PNML file removed")


def export_to_json(net, initial_marking, final_marking):
    logging.info("Exporting Petri net to JSON")

    places = [{"id": place.name, "resource": place.properties.get('resource', '')} for place in net.places]
    transitions = [{"id": trans.name, "label": trans.label, "resource": trans.properties.get('resource', '')} for trans in net.transitions]
    arcs = [{"source": arc.source.name, "target": arc.target.name} for arc in net.arcs]

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

async def run_split_miner(file_content):
    temp_file_path = 'temp_log.xes'
    try:
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
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)