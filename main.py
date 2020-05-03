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

class Tab:
    cid: int
    tot: int

   
#zadanie_5:
@app.get("/sales")
async def sale(category): 
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('SELECT customerid,total FROM invoices').fetchall()
    T=[]
    t=[]
    i=0
    while i<len(data):
        t.append(data[i][0])
        t.append(data[i][1])
        t[1]=round(t[1],2)
        licz=0
        for j in T:
            if j[0]==t[0]:
                j[1]+=t[1]
                licz+=1
        if licz==0:
            T.append(t)
        t=[]
        i+=1
    return T
