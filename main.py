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

	

@app.get("/tracks")#,response_model = Track)
async def db_task_1(page: int = 0, per_page: int = 10):
	cursor = app.db_connection.cursor()
	tracks = cursor.execute(f"SELECT * FROM tracks WHERE TrackId <= {per_page*(page+1)} AND TrackId > {per_page*page}").fetchall()
	tracks_list = []
	for i in tracks:

		tracks_list.append(Track(
			TrackId=i[0],
			Name=i[1],
			AlbumId=i[2],
			MediaTypeId=i[3],
			GenreId=i[4],
			Composer=i[5],
			Milliseconds=i[6],
			Bytes=i[7],
			UnitPrice=i[8]
			))
	print(len(tracks_list))
	return tracks_list

'''      
@app.get("/tracks")
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

class ResponseTask4(BaseModel):
	CustomerId: int = None
	FirstName: str = None
	LastName: str = None
	Company: str = None
	Address: str = None
	City: str = None
	State: str = None
	Country: str = None
	PostalCode: str = None
	Phone: str = None
	Fax: str = None
	Email: str = None
	SupportRepId: int = None
		
from fastapi.encoders import jsonable_encoder


@app.put("/customers/{customer_id}")
async def db_task_4(customer_id: int,data: dict):
	cursor = app.db_connection.cursor()
	is_customer_exist = cursor.execute("SELECT CustomerId FROM customers WHERE CustomerId=:id",{"id": customer_id}).fetchall()
	if len(is_customer_exist) == 0:
		item={"detail": {"error":str(customer_id)} }
		return JSONResponse(status_code=404,content=item)
	for i in data:
		cursor.execute(f"UPDATE customers SET {i} = :value WHERE CustomerId=:id",
			{"value": data[i], "id": customer_id})	
	client = cursor.execute("SELECT * FROM customers WHERE CustomerId=:id",{"id": customer_id}).fetchall()
	content = ResponseTask4(
		CustomerId = client[0][0],
		FirstName = client[0][1],
		LastName= client[0][2],
		Company= client[0][3],
		Address= client[0][4],
		City = client[0][5],
		State = client[0][6],
		Country = client[0][7],
		PostalCode = client[0][8],
		Phone = client[0][9],
		Fax = client[0][10],
		Email = client[0][11],
		SupportRepId = client[0][12]
		)
	return JSONResponse(status_code=200,content=jsonable_encoder(content))



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
