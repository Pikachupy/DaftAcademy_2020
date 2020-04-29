
import sqlite3
from fastapi import FastAPI
from fastapi import Depends, Cookie, HTTPException

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

'''   
@app.get("/tracks")
async def getgtracks():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('SELECT * FROM tracks ORDER BY TrackId LIMIT 10 OFFSET 0').fetchall()
    return data
    
'''

@app.get("/tracks/composers/")
async def tracks_with_comp():
    app.db_connection.row_factory = sqlite3.Row
    composer_name='Miles Davis'
    tup=composer_name
    data = app.db_connection.execute('SELECT name FROM tracks WHERE composer=Miles Davis ORDER BY name').fetchall()
    return data


        
