from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Response, status
from fastapi import Depends, Cookie, HTTPException
from hashlib import sha256
import secrets

app = FastAPI()

@app.get('/welcome')
def get_welcome():
	return {"message": "Hello World during the coronavirus pandemic!"}


app.secret_key = "very constatn and random secret, best 64 characters"
app.tokens = []
security = HTTPBasic()


def user(credentials: HTTPBasicCredentials = Depends(security)):
	correct_username = secrets.compare_digest(credentials.username, 'trudnY')
	correct_password = secrets.compare_digest(credentials.password, 'PaC13Nt')
	if not (correct_username and correct_password):
		raise HTTPException(status_code = 401)
	else:
		s_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
		return s_token

	
@app.post('/login')
def login(response: Response, s_token = Depends(user)):
	app.tokens += s_token
	response.set_cookie(key="s_token", value=s_token)
	response = RedirectResponse(url = '/welcome')
	response.status_code = 302
	return response
