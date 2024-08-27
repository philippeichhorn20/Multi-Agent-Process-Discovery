from fastapi import FastAPI, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from typing import Optional
from discover.discover import run_split_miner, run_inductive_miner
import logging
import asyncio

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