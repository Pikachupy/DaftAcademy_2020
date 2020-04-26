from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Response, status
from fastapi import Depends, Cookie, HTTPException
from hashlib import sha256

import secrets


app = FastAPI()


@app.get("/welcome")
def get_welcome():
	return "Hello!"


app.secret_key = "very constatn and random secret, best 64 characters"
app.tokens = []
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
	correct_username = secrets.compare_digest(credentials.username, "trudnY")
	correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
	print(f"{credentials.username}")
	print(f"{credentials.password}")
	if not (correct_username and correct_password):
		raise HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		)
	else:
		session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
		return session_token
    



@app.post("/login")
def login(
	response: Response,
	session_token = Depends(get_current_username)
	):
    
	app.tokens+=(session_token)
    
	response.set_cookie(key="session_token", value=session_token)
    
        
	response = RedirectResponse(url = "/welcome")
	response.status_code = status.HTTP_302_FOUND
    
	return response
