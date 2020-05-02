import sqlite3
from fastapi import FastAPI
from fastapi import Depends, Cookie, HTTPException, Response
import secrets
from fastapi import status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from fastapi.responses import JSONResponse
from typing import Set

import jose
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

app = FastAPI()

security = HTTPBasic()

from pydantic import BaseModel

class Album(BaseModel):
    title: str
    artist_id: int


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

    
#zadanie_1: xxx
class Item(BaseModel):
    per_page: int = 10
    page: int = 0

        
@app.get("/tracks/?{cos}")
async def getgtracks():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('SELECT * FROM tracks ORDER BY TrackId LIMIT ? OFFSET ?',(item,item)).fetchall()                  
    return data
    
    
#zadanie_2:
@app.get("/tracks/composers/")
async def tracks_with_comp(composer_name): 
    app.db_connection.row_factory = lambda cursor, x: x[0]
    tup=(composer_name,)
    data = app.db_connection.execute('SELECT name FROM tracks WHERE composer LIKE ? ORDER BY name',tup).fetchall()
    if data ==[]:
        raise HTTPException(
        status_code=404,
        detail="error",
        )
    return data


#zadanie_3:
@app.post("/albums")
async def addalbum(album: Album):
    app.db_connection.row_factory = lambda cursor, x: x[0]
    data2 = app.db_connection.execute('SELECT artistid FROM albums').fetchall()
    if not (album.artist_id in data2):
        raise HTTPException(
        status_code=404,
        detail="error",
        )
    cursor = app.db_connection.execute('INSERT INTO albums (title,artistid) VALUES (?,?)',(album.title,album.artist_id))
    app.db_connection.commit()
    new_album_id = cursor.lastrowid
    app.db_connection.row_factory = sqlite3.Row
    item={"AlbumId": new_album_id, "Title": album.title, "ArtistId": album.artist_id}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)


@app.get("/albums/{album_id}")
async def albid(album_id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(f'SELECT albumid,title,artistid FROM albums WHERE albumid={album_id}').fetchone()
    return data
    
#zadanie_4: xxx
class Customer(BaseModel):
    CustomerId: int
    FirstName: str
    LastName: str
    Company: str
    Address: str
    City: str
    State: str
    Country: str
    PostalCode: str
    Phone: str
    Fax: str
    Email: str
    SupportRepId: int
  
@app.put("/customers/{customer_id}")
async def cust(customer_id: int, customer: Customer):
    app.db_connection.row_factory = lambda cursor, x: x[0]
    data2 = app.db_connection.execute('SELECT customerid FROM customers').fetchall()
    if not (customer_id in data2):
        item={"detail": {"error":str(customer_id)} }
        return JSONResponse(status_code=404, content=item)

    
#zadanie_5:
@app.get("/sales")
async def sale(category): 
    app.db_connection.row_factory = lambda cursor, x: x[0]
    tup=(composer_name,)
    data = app.db_connection.execute('SELECT name FROM tracks WHERE composer LIKE ? ORDER BY name',tup).fetchall()
    if data ==[]:
        raise HTTPException(
        status_code=404,
        detail="error",
        )
    return data
