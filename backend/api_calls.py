from fastapi import FastAPI, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import  Response
from typing import Optional
from discover import  run_inductive_miner_basic, run_split_miner_basic, run_miner_compose
import logging
from fastapi import UploadFile,  HTTPException
import json
from stats import alignment_fitness, alignment_precision, entropy_based_fitness, entropy_based_precision, entropy_based_precision_old
from discover import export_to_pnml
from NetStorer import NetStorer
from InteractionUtils import InteractionUtils
from isomororph_check import matching_ip
import os

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

'''
This class contains the only hook, in this appliation
Inputs:
file: XES log file
algorithm: "inductive" or "split" miner
use_compositional: apply interaction aware approach outlined in the paper
entropy_metrics: flag do indicate the metrics are wanted
alignment_metrics: s.a.

Returns:
net: the resulting net
abstract_net: the underlying interaction pattern (only compositional)
matching_ip: if exists, the underlying IP-Protocol pattern
statistics: if requested
'''


@app.post("/discover")
async def discover_process(
    file: UploadFile,
    algorithm: str = Form(...),
    use_compositional: bool =Form(...),
    noise_threshold: Optional[float] = Form(None),
    entropy_metrics: bool =Form(...),
    alignment_metrics: bool =Form(...)
):
    logging.info(f"Received discovery request. Algorithm: {algorithm}")
    try:
        composed_nets = None
        net_storage = await NetStorer.create(file)
        net, im, fm, a_net, a_im, a_fm = None, None, None, None, None, None
        if(use_compositional):
           composed_nets = await run_miner_compose(net_storage, noise_threshold, algorithm)
           net, im, fm, a_net, a_im, a_fm = composed_nets

        else:
            if algorithm == "split":
                net, im, fm, = await run_split_miner_basic(net_storage, noise_threshold)
            elif algorithm == "inductive":
                if noise_threshold is None:
                    raise ValueError("Noise threshold is required for inductive miner")
                net, im, fm, = await run_inductive_miner_basic(net_storage, noise_threshold)

        matching_ip_string = ""
        if a_net:
            print("abstract net found")
            matching_ip_string = matching_ip(a_net)
        else:
            print("abstract net not found")

        response = {
            "stats":{
                'matching ip': matching_ip_string,
            }
        }


        try:
            if entropy_metrics:
                entropy_precision, entropy_recall = entropy_based_precision(net_storage=net_storage, net=net, initial=im, final=fm, )
                response["stats"]["entropy precision"] = entropy_precision
                response["stats"]["entropy recall"] = entropy_recall
        except Exception as e:
            logging.error(f"Error during entropy metrics calculation: {str(e)}")
            response["stats"]["entropy error"] = str(e)


        try:
            if alignment_metrics:
                precision = alignment_precision(net, net_storage.df, im, fm) # todo uncomment, but takes long
                fitness = alignment_fitness(net, net_storage.df, im, fm)
                response["stats"]["alignment precision"] = precision
                response["stats"]["alignment fitness"] = fitness["averageFitness"]
        except Exception as e:
            logging.error(f"Error during alignment metrics calculation: {str(e)}")
            response["stats"]["alignment error"] = str(e)

        InteractionUtils.encode_names_for_transfer(net)
        pnml = export_to_pnml(net, im, fm)
        response["net"] = pnml

        if a_net: 
            InteractionUtils.encode_names_for_transfer(a_net)
            abstract_net_pnml = export_to_pnml(a_net, a_im, a_fm)
            response["abstract_net"] = abstract_net_pnml

        logging.info("Discovery process completed, preparing response")

        return Response(content=json.dumps(response), media_type="application/xml")
        
    except Exception as e:
        logging.error(f"Error during discovery: {str(e)}")
        logging.error(str(e.with_traceback))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists('temp_log.xes'):
            os.remove('temp_log.xes')
        logging.info("Request handling completed")
