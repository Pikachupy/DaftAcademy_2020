
import sqlite3
from fastapi import FastAPI
from fastapi import Depends, Cookie, HTTPException, Response

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

  
@app.get("/tracks")
async def getgtracks():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('SELECT * FROM tracks ORDER BY TrackId LIMIT 10 OFFSET 0').fetchall()
    return data
    


@app.get("/tracks/composers/")
async def tracks_with_comp(composer_name):
    app.db_connection.row_factory = lambda cursor, x: x[0]
    data2 = app.db_connection.execute('SELECT composer FROM tracks').fetchall()
    if composer_name in data2:       
        app.db_connection.row_factory = lambda cursor, x: x[0]
        composer_name+='%'
        tup=(composer_name,)
        data = app.db_connection.execute('SELECT name FROM tracks WHERE composer LIKE ? ORDER BY name',tup).fetchall()
        return data
    else:
        return Response(status_code=status.404)

       
        


        
