from fastapi import FastAPI
from .router import router as process_router


"""
command to run

cd app
uvicorn main:app --reload

swagger is avaiable at url:

http://127.0.0.1:8000/docs

"""

app = FastAPI()
app.include_router(process_router)
