import uvicorn


def main():
    uvicorn.run("project.app.main:app", host="127.0.0.1", port=8000, reload=True)
