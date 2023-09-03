from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root() -> str:
    return "The backend is up"
