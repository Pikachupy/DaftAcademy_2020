from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Response, status
from fastapi import Depends, Cookie, HTTPException
from hashlib import sha256
import secrets
from starlette.responses import HTMLResponse

from starlette.authentication import requires
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)


app = FastAPI()


@app.get('/')
def get_welcome():
	return {"message": "Hello!"}

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
		return s_token, AuthCredentials(["authenticated"]), SimpleUser(credentials.username)


@app.get('/welcome')
def get_welcome(response: Response, s_token: str = Depends(user)):
	if s_token is None:
		response.status_code = 401
		return "You are not allowed to be here!"
	response = HTMLResponse('<html><body><h1><div id="greeting">Hello, {{ user }}!</div></h1></body></html>')
	response.status_code = 302
	return response
	
	
	
@app.post('/login')
def login(response: Response,s_token = Depends(user)):
	app.tokens += s_token
	response.set_cookie(key="s_token", value=s_token)
	response = RedirectResponse(url = '/welcome')
	response.status_code = 302
	return response


@app.post('/logout')
def logout(response: Response):
	response = RedirectResponse(url = '/')
	response.status_code = 302
	return response
	
