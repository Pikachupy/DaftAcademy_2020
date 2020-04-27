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


    
@app.get("/tracks/composers/")
async def tracks_with_comp(composer_name):
    try:
        app.db_connection.row_factory = sqlite3.Row
        query =''' SELECT name FROM tracks WHERE artist = composer_name '''
        data = app.db_connection.execute(query).fetchall()
        return data
    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))

    
    
