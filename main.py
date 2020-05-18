#1st

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


@app.api_route(path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"])
def read_request(request: Request):
    return {"method": request.method}


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

#3rd
import secrets
from typing import Dict, Optional

from fastapi import Depends, FastAPI, Response, status, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import APIKeyCookie, HTTPBasic, HTTPBasicCredentials
from jose import jwt
from pydantic import BaseModel
from starlette.responses import RedirectResponse


class Patient(BaseModel):
    name: str
    surname: str


class DaftAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter: int = 0
        self.storage: Dict[int, Patient] = {}
        self.security = HTTPBasic(auto_error=False)
        self.secret_key = "kluczyk"
        self.API_KEY = "session"
        self.cookie_sec = APIKeyCookie(name=self.API_KEY, auto_error=False)
        self.templates = Jinja2Templates(directory="templates")


app = DaftAPI()


def is_logged(session: str = Depends(app.cookie_sec), silent: bool = False):
    try:
        payload = jwt.decode(session, app.secret_key)
        return payload.get("magic_key")
    except Exception:
        pass

    if silent:
        return False

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def authethicate(credentials: Optional[HTTPBasicCredentials] = Depends(app.security)):
    if not credentials:
        return False

    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")

    if not (correct_username and correct_password):
        return False
    return True


@app.get("/")
def read_root():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/welcome")
def welcome(request: Request, is_logged: bool = Depends(is_logged)):
    return app.templates.TemplateResponse(
        "welcome.html", {"request": request, "user": "trudnY"}
    )


@app.post("/login")
async def login_basic(auth: bool = Depends(authethicate)):
    if not auth:
        response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
        return response

    response = RedirectResponse(url="/welcome")
    token = jwt.encode({"magic_key": True}, app.secret_key)
    response.set_cookie("session", token)
    return response


@app.post("/logout")
async def logout(is_logged: bool = Depends(is_logged)):
    response = RedirectResponse(url="/")
    response.delete_cookie("session")
    return response


@app.post("/patient")
def add_patient(patient: Patient, is_logged: bool = Depends(is_logged)):
    app.storage[app.counter] = patient
    response = RedirectResponse(url=f"/patient/{app.counter}")
    app.counter += 1
    return response


@app.get("/patient")
def show_patients(is_logged: bool = Depends(is_logged)):
    return app.storage


@app.get("/patient/{pk}")
def show_patient(pk: int, is_logged: bool = Depends(is_logged)):
    if pk in app.storage:
        return app.storage.get(pk)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/patient/{pk}")
def delte_patient(pk: int, is_logged: bool = Depends(is_logged)):
    if pk in app.storage:
        del app.storage[pk]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#4th
'''
from fastapi import FastAPI, HTTPException, status

import crud
from schemas import AlbumItem, CustomerItem

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Do or do not. There is no try. # Yoda"}


@app.get("/tracks")
def all_tracks(page: int = 0, per_page: int = 10):
    return crud.get_all_trucks(per_page, page)


@app.get("/tracks/composers")
def all_composer_tracks(composer_name: str):
    data = crud.get_all_composer_tracks(composer_name)
    if data:
        response = [elem["Name"] for elem in data]
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "The given composer was not found."},
        )


@app.post("/albums", status_code=status.HTTP_201_CREATED)
def post_new_album(item: AlbumItem):
    artist = crud.get_artist_by_id(item.artist_id)
    if artist:
        new_album = crud.add_new_album(item.title, item.artist_id)
        new_album_id = new_album.lastrowid
        return crud.get_album_by_id(new_album_id)

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "The given artist_id was not found."},
        )


@app.get("/albums/{album_id}")
def get_album(album_id: int):
    return crud.get_album_by_id(album_id)


@app.put("/customers/{customer_id}")
def put_customer_info(customer_id: str, item: CustomerItem):
    customer = crud.get_customer_by_id(customer_id)
    if customer:
        sql_placeholders = []
        sql_params = []
        update_data = item.dict(exclude_unset=True)
        [
            [sql_placeholders.append(f"{k} = ?"), sql_params.append(v)]
            for k, v in update_data.items()
        ]
        sql_params.append(customer_id)
        sql_placeholders = ", ".join(sql_placeholders)

        return crud.edit_customer_info(customer_id, sql_placeholders, sql_params)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "The given customer was not found."},
        )


@app.get("/sales")
def customers_expenses(category: str):
    statistics = {
        "customers": crud.get_statistic_customers,
        "genres": crud.get_statistic_genres,
    }

    if category and category in statistics:
        data = statistics[category]()
        return data

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "The given category was not found."},
        )


"uvicorn main:app --reload"
'''
