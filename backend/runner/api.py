from fastapi import APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import Response
from runner.discover import run_discovery

router = APIRouter()

@router.post("/discover")
async def discover_process(
    file: UploadFile,
    algorithm: str = Form(...),
    use_compositional: bool = Form(...),
    noise_threshold: float = Form(None),
    entropy_metrics: bool = Form(...),
    alignment_metrics: bool = Form(...),
):
    return await run_discovery(
        file,
        algorithm,
        use_compositional,
        noise_threshold,
        entropy_metrics,
        alignment_metrics
    )
