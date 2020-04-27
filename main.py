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
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
     SELECT * FROM Tracks ORDER BY TrackId LIMIT''' + str(per_page) + '''OFFSET''' + str(page);
     ).fetchall()
    return data
