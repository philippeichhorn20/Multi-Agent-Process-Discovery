import logging
from pm4py import discover_petri_net_inductive
from services.log_store import LogStore

async def run_inductive_miner_basic(log_storage: LogStore, noise_threshold):
    print(f"Basic: Starting Inductive Miner basic with noise threshold {noise_threshold}")
    try:
        if not noise_threshold:
            noise_threshold = 0
        net, im, fm = discover_petri_net_inductive(log_storage.df, noise_threshold=noise_threshold)

    except Exception as e:
        logging.error(f"Error during discoveryn inductive: {str(e)}")
        raise
    return net, im, fm



