import os
import json
import logging
from typing import Optional, Dict, Any, Tuple

from fastapi import  HTTPException
from fastapi.responses import Response

from core.utils import export_to_pnml
from core.miners.miner import run_miner
from core.miners import run_split_miner_basic, run_inductive_miner_basic, run_miner_compose
from core.metrics import alignment_fitness, alignment_precision, entropy_based_precision

from services.log_store import LogStore
from core.miners.interaction_utils import InteractionUtils
from services.isomororph_check import find_matching_interaction_pattern


async def run_discovery(
    file,
    algorithm,
    use_compositional,
    noise_threshold,
    entropy_metrics,
    alignment_metrics
):
    try:
        log_storage = await LogStore.store(file)
        mined_nets = await run_miner(log_storage, algorithm, noise_threshold, use_compositional)

        # Unpack results depending on miner type
        if use_compositional:
            net, im, fm, a_net, a_im, a_fm = mined_nets
        else:
            net, im, fm = mined_nets
            a_net = a_im = a_fm = None

		
        # Prepare stats


        
        interaction_pattern = find_matching_interaction_pattern(a_net) if a_net else ""
    

        response = {
            "stats":{
                'matching ip': interaction_pattern,
            }
        }
        if entropy_metrics:
            add_entropy_metrics(response, log_storage, net, im, fm)

        if alignment_metrics:
            add_alignment_metrics(response, log_storage, net, im, fm)

        # Add PNML exports
        response["net"] = prepare_pnml(net, im, fm)
        if a_net:
            response["abstract_net"] = prepare_pnml(a_net, a_im, a_fm)

        logging.info("Discovery process completed successfully")
        return Response(content=json.dumps(response), media_type="application/xml")

    except ValueError as ve:
        logging.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.exception("Unexpected error during discovery process")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup_temp_files()





def add_entropy_metrics(response: Dict[str, Any], log_storage, net, im, fm) -> None:
    """Add entropy-based metrics to the response."""
    try:
        entropy_precision, entropy_recall = entropy_based_precision(
            log_storage=log_storage,
            net=net,
            initial=im,
            final=fm
        )
        response["stats"]["entropy precision"] = entropy_precision
        response["stats"]["entropy recall"] = entropy_recall
    except Exception as e:
        logging.error(f"Error during entropy metrics calculation: {e}")
        response["stats"]["entropy error"] = str(e)


def add_alignment_metrics(response: Dict[str, Any], log_storage, net, im, fm) -> None:
    """Add alignment-based metrics to the response."""
    try:
        precision = alignment_precision(net, log_storage.df, im, fm)
        fitness = alignment_fitness(net, log_storage.df, im, fm)
        response["stats"]["alignment precision"] = precision
        response["stats"]["alignment fitness"] = fitness["averageFitness"]
    except Exception as e:
        logging.error(f"Error during alignment metrics calculation: {e}")
        response["stats"]["alignment error"] = str(e)


def prepare_pnml(net, im, fm) -> str:
    """Encode names and export net to PNML."""
    InteractionUtils.encode_names_for_transfer(net)
    return export_to_pnml(net, im, fm)


def cleanup_temp_files() -> None:
    """Remove temporary files created during request processing."""
    if os.path.exists("temp_log.xes"):
        os.remove("temp_log.xes")
    logging.info("Temporary files cleaned up")

