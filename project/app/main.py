from fastapi import APIRouter, FastAPI
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
