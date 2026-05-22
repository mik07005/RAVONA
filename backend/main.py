from fastapi import FastAPI
from pydantic import BaseModel

from core.controller import process_input

app = FastAPI()

class InputRequest(BaseModel):
    input: str

@app.get("/")
def home():
    return {
        "message": "AURA X Backend Running"
    }

@app.post("/input")
def handle_input(request: InputRequest):

    response = process_input(request.input)

    return {
        "response": response
    }