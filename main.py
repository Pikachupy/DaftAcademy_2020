from typing import Dict

from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel
from starlette.authentication import requires
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route
import base64
import binascii

app = FastAPI()
app.counter: int = 0
app.storage: Dict[int, Patient] = {}
app.users={"admin":"admin"}

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return
        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        # TODO: You'd want to verify the username and password here.
        if username in app.users and password == app.users[username]:
            return AuthCredentials(["authenticated"]), SimpleUser(username)
        else:
            raise HTTPException(status_code=403, detail="Unathorised")
            

@app.get("/")
async def homepage(request):
    if request.user.is_authenticated:
        return PlainTextResponse('Hello, ' + request.user.display_name)
    return PlainTextResponse('Hello, you')

class Patient(BaseModel):
    name: str
    surename: str



@requires(['authenticated'], status_code=404)
@app.get("/")
def read_root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@requires(['authenticated'], status_code=404)
@app.get("/welcome")
def read_root():
    return {"message": "Hey Hi Hello!"}

@requires(['authenticated'], status_code=404)
@app.api_route(path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"])
def read_request(request: Request):
    return {"method": request.method}

@requires(['authenticated'], status_code=404)
@app.post("/patient")
def show_data(patient: Patient):
    resp = {"id": app.counter, "patient": patient}
    app.storage[app.counter] = patient
    app.counter += 1
    return resp

@requires(['authenticated'], status_code=404)
@app.get("/patient/{pk}")
def show_patient(pk: int):
    if pk in app.storage:
        return app.storage.get(pk)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
