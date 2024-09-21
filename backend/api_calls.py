from fastapi import FastAPI, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from typing import Optional
from discover import run_split_miner_compose, run_inductive_miner_basic, run_split_miner_basic
import logging
import asyncio
from fastapi import UploadFile, File, HTTPException, BackgroundTasks
from refinement_algorithm import are_petri_nets_isomorphic
import json
from pm4py.objects.petri_net.obj import PetriNet, Marking
from stats import alignment_fitness, alignment_precision, entropy_based_fitness, entropy_based_precision
from discover import export_to_pnml
import pm4py
from NetStorer import NetStorer

# fastapi dev api_calls.py

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods if needed
    allow_headers=["*"],  # You can specify specific headers if needed
)

@app.post("/discover")
async def discover_process(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    algorithm: str = Form(...),
    noise_threshold: Optional[float] = Form(None)
):
    logging.info(f"Received discovery request. Algorithm: {algorithm}")
    try:
        net_storage = await NetStorer.create(file)
        if algorithm == "split":
            result = await run_split_miner_basic(net_storage, noise_threshold)
        elif algorithm == "inductive":
            if noise_threshold is None:
                raise ValueError("Noise threshold is required for inductive miner")
            result = await run_inductive_miner_basic(net_storage, noise_threshold)
        else:
            raise ValueError("Invalid algorithm specified")
        net, im, fm = result
        # precision = alignment_precision(net, df, im, fm) # todo uncomment, but takes long
        # fitness = alignment_fitness(net, df, im, fm)
        # entropy_precision = entropy_based_precision()
        pnml = export_to_pnml(net, im, fm)

        logging.info("Discovery completed successfully")
        logging.info("Discovery process completed, preparing response")
        response = {
            "net": pnml,
            "stats":{
                # "precision": precision,
                # "fitness": fitness,  
            }
        }
        return Response(content=json.dumps(response), media_type="application/xml")
        
    except Exception as e:
        logging.error(f"Error during discovery: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logging.info("Request handling completed")

# def json_to_petri_net(json_data):

#     net = PetriNet(name=json_data.get('name', 'Converted Petri Net'))
    
#     # Create places
#     places = {}
#     for place_data in json_data.get('places', []):
#         place = PetriNet.Place(name=place_data['id'])
#         net.places.add(place)
#         places[place_data['id']] = place
#     # Create transitions
#     transitions = {}
#     for transition_data in json_data.get('transitions', []):
#         transition = PetriNet.Transition(name=transition_data['id'], label=transition_data.get('label'))
#         net.transitions.add(transition)
#         transitions[transition_data['id']] = transition

#     # Create arcs
#     for arc_data in json_data.get('arcs', []):
#         source = places.get(arc_data['sourceId']) or transitions.get(arc_data['sourceId'])
#         target = places.get(arc_data['targetId']) or transitions.get(arc_data['targetId'])
#         if source and target:
#             arc = PetriNet.Arc(source, target)
#             net.arcs.add(arc)

#     # Create initial marking
#     # initial_marking = Marking()
#     # for place_id, tokens in json_data.get('initialMarking', {}).items():
#     #     if place_id in places:
#     #         initial_marking[places[place_id]] = tokens
#     # print("bhefic")

#     # # Create final marking
#     # final_marking = Marking()
#     # for place_id, tokens in json_data.get('finalMarking', {}).items():
#     #     if place_id in places:
#     #         final_marking[places[place_id]] = tokens

#     return net
