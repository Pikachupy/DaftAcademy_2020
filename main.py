import sqlite3
from fastapi import FastAPI


app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/tracks")
async def tracks_with_artist(page=0, per_page=10):
    try:
        app.db_connection.row_factory = sqlite3.Row
        query = '''SELECT * FROM Tracks ORDER BY TrackId LIMIT %s OFFSET %s'''
        params = (per_page, page)
        data = app.db_connection.execute(query, params).fetchall()
        return data
    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))
