import os

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .endpoints.art_ideas import router as router_ideas

router = APIRouter()
router.include_router(router_ideas)

"""
command to run

cd app
uvicorn main:app --reload

swagger is avaiable at url:

http://127.0.0.1:8000/docs

"""

app = FastAPI()
app.include_router(router)


origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
