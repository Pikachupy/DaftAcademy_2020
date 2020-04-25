# main.py

from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello Wurld!!!"}


@pytest.mark.parametrize("name", ['Zenek', 'Marek', 'Alojzy Niezdąży'])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.text == f'"Hello {name}"'
