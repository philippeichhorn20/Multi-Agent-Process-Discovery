
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from runner.api import router

app = FastAPI()

ALLOWED_ORIGINS = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=router)
