import os

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .endpoints.art_ideas import router as router_ideas
from .endpoints.reference_material import router as router_reference

router = APIRouter()
router.include_router(router_ideas)
router.include_router(router_reference)

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
