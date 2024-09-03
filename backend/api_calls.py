from fastapi import FastAPI, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from typing import Optional
from backend.discover import run_split_miner, run_inductive_miner
import logging
import asyncio
import io
from fastapi import UploadFile, File, HTTPException, BackgroundTasks
import pm4py
from discover.refinement_algorithm import are_petri_nets_isomorphic
import json
from pm4py.objects.petri_net.obj import PetriNet, Marking

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

async def process_discovery(file_content, algorithm, noise_threshold):
    try:
        if algorithm == "split":
            result = await run_split_miner(file_content)
        elif algorithm == "inductive":
            if noise_threshold is None:
                raise ValueError("Noise threshold is required for inductive miner")
            result = await run_inductive_miner(file_content, noise_threshold)
        else:
            raise ValueError("Invalid algorithm specified")
        
        logging.info("Discovery completed successfully")
        return result
    except Exception as e:
        logging.error(f"Error during discovery: {str(e)}")
        raise

@app.post("/discover")
async def discover_process(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    algorithm: str = Form(...),
    noise_threshold: Optional[float] = Form(None)
):
    logging.info(f"Received discovery request. Algorithm: {algorithm}")
    try:
        file_content = await file.read()
        logging.info(f"File read successfully. Size: {len(file_content)} bytes")
        
        result_future = asyncio.create_task(process_discovery(file_content, algorithm, noise_threshold))
        
        try:
            result = await asyncio.wait_for(result_future, timeout=110)
            logging.info("Discovery process completed, preparing response")
            return Response(content=result, media_type="application/xml")
        except asyncio.TimeoutError:
            logging.error("Discovery process timed out")
            raise HTTPException(status_code=504, detail="The discovery process timed out. Please try with a smaller file or contact the administrator.")
        
    except Exception as e:
        logging.error(f"Error during discovery: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logging.info("Request handling completed")

@app.post("/check_isomorphism")
async def check_petri_nets_isomorphism(
    background_tasks: BackgroundTasks,
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    logging.info("Received isomorphism check request")
    try:
        # Read the contents of both files
        content1 = json.loads(await file1.read())
        content2 = json.loads(await file2.read())
        
        # Convert JSON to PetriNet objects
        net1 = json_to_petri_net(content1)
        net2 = json_to_petri_net(content2)
        
        # Perform the isomorphism check
        is_isomorphic = are_petri_nets_isomorphic(net1, net2)
        
        logging.info(f"Isomorphism check completed. Result: {is_isomorphic}")
        return {"isomorphic": is_isomorphic}
    
    except Exception as e:
        logging.error(f"Error during isomorphism check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logging.info("Isomorphism check request handling completed")

def json_to_petri_net(json_data):

    net = PetriNet(name=json_data.get('name', 'Converted Petri Net'))
    
    # Create places
    places = {}
    for place_data in json_data.get('places', []):
        place = PetriNet.Place(name=place_data['id'])
        net.places.add(place)
        places[place_data['id']] = place
    # Create transitions
    transitions = {}
    for transition_data in json_data.get('transitions', []):
        transition = PetriNet.Transition(name=transition_data['id'], label=transition_data.get('label'))
        net.transitions.add(transition)
        transitions[transition_data['id']] = transition

    # Create arcs
    for arc_data in json_data.get('arcs', []):
        source = places.get(arc_data['sourceId']) or transitions.get(arc_data['sourceId'])
        target = places.get(arc_data['targetId']) or transitions.get(arc_data['targetId'])
        if source and target:
            arc = PetriNet.Arc(source, target)
            net.arcs.add(arc)

    # Create initial marking
    # initial_marking = Marking()
    # for place_id, tokens in json_data.get('initialMarking', {}).items():
    #     if place_id in places:
    #         initial_marking[places[place_id]] = tokens
    # print("bhefic")

    # # Create final marking
    # final_marking = Marking()
    # for place_id, tokens in json_data.get('finalMarking', {}).items():
    #     if place_id in places:
    #         final_marking[places[place_id]] = tokens

    return net
