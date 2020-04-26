from typing import Dict

from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel


class Patient(BaseModel):
    name: str
    surename: str


app = FastAPI()
app.counter: int = 0
app.storage: Dict[int, Patient] = {}


@app.get("/")
def read_root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/welcome')
def read_root():
    return {"message": "Helloooo!"}

@app.api_route(path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"])
def read_request(request: Request):
    return {"method": request.method}


class log(BaseModel):
    first_key: str
        
class resp(BaseModel):
    received: Dict

@app.post("/login", response_model=resp)
def receive_something(rq: log):
    return log(received=rq.dict())


@app.post("/patient")
def show_data(patient: Patient):
    resp = {"id": app.counter, "patient": patient}
    app.storage[app.counter] = patient
    app.counter += 1
    return resp


@app.get("/patient/{pk}")
def show_patient(pk: int):
    if pk in app.storage:
        return app.storage.get(pk)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
