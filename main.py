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
class CustomerStat(BaseModel):
	CustomerId: int = None
	Email: str = None
	Phone: str = None
	Sum: float = None

class GenresStat(BaseModel):
	Name: str = None
	Sum: int = None

@app.get("/sales")
async def db_task_5(category: str=None):
	if category == "customers":
		cursor = app.db_connection.cursor()
		data = cursor.execute("""
			SELECT CustomerId, Email, Phone, ROUND(SUM(Total),2) as Sum FROM(
			SELECT * FROM invoices  
			JOIN customers ON customers.CustomerId = invoices.CustomerId
			)GROUP BY CustomerId ORDER BY Sum DESC, CustomerId ASC
			""").fetchall()
		content = []
		for i in data:
			content.append(CustomerStat(
				CustomerId = i[0],
				Email = i[1],
				Phone = i[2],
				Sum = round(i[3],2)
				))
		return content
	elif category == "genres":
		cursor = app.db_connection.cursor()
		app.db_connection.row_factory = sqlite3.Row
		data = cursor.execute("""
			SELECT Name, COUNT(GenreId) AS SUM FROM (
			SELECT * FROM genres 
			JOIN tracks ON tracks.GenreId = genres.GenreId
			JOIN invoice_items ON invoice_items.TrackId = tracks.TrackId
			)GROUP BY GenreId ORDER BY Sum,customerid DESC, Name ASC
			""").fetchall()
		item={"AlbumId": new_album_id, "Title": album.title, "ArtistId": album.artist_id}
		content = []
		for i in data:
			content.append(GenresStat(
				Name = i[0],
				Sum = i[1],
				))
		return content
	else:
		item={"detail": {"error":str(category)} }
		return JSONResponse(status_code=404,content=item)
 

'''
@app.get("/sales")
async def sale(category): 
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('SELECT customerid,total FROM invoices').fetchall()
    T=[]
    t=[]
    i=0
    while i<len(data):
        t.append(data[i][0])
        t.append(float(data[i][1]))
        licz=0
        t[1]=round(t[1],2)
        for j in T:
            if j[0]==t[0]:
                j[1]+=t[1]
                j[1]=round(j[1],2)
                licz+=1
              
        if licz==0:
            T.append(t)
        t=[]
        i+=1
    return T
'''
