from typing import Optional, Dict, Any, Tuple
from core.miners import run_split_miner_basic, run_inductive_miner_basic, run_miner_compose
from services.log_store import LogStore


async def run_miner(
    log_storage: LogStore,
    algorithm: str,
    noise_threshold: Optional[float],
    use_compositional: bool
) -> Tuple:
    """Run the appropriate process discovery algorithm."""
    if use_compositional:
        return await run_miner_compose(log_storage, noise_threshold, algorithm)
    if algorithm == "split":
        return await run_split_miner_basic(log_storage, noise_threshold)
    elif algorithm == "inductive":
        if noise_threshold is None:
            raise ValueError("Noise threshold is required for inductive miner")
        return await run_inductive_miner_basic(log_storage, noise_threshold)

    raise ValueError(f"Unknown algorithm: {algorithm}")