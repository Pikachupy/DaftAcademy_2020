from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Response, status
from fastapi import Depends, Cookie, HTTPException
from hashlib import sha256

import secrets
import requests

app = FastAPI()

@app.post('/welcome')
@app.get('/welcome')
def get_welcome():
	return  {"message": "Welcome"}


app.secret_key = "very constatn and random secret, best 64 characters"
app.tokens = []

@app.get('/login')
@app.post("/login/")
def create_cookie(user: str, password: str, response: Response):
	try :
		if user == 'trudnY' and password == 'PaC13Nt':
			session_token = sha256(bytes(f"{user}{password}{app.secret_key}")).hexdigest()
			app.tokens+=session_token
			response = RedirectResponse(url='/welcome')
			response.set_cookie(key="session_token", value=session_token)
			response.status_code=302
			return response
		else:
			raise AuthenticationError('Invalid basic auth credentials')
	except KeyError: 
		raise HTTPException(401,"User does not exists")
		
'''
@app.get("/data/")
def create_cookie(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.tokens :
        raise HTTPException(status_code=403, detail="Unathorised")
    response.set_cookie(key="session_token", value=session_token)

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    print(f"{credentials.username}")
    print(f"{credentials.password}")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # detail="Incorrect email or password",
            # headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username



@app.post('/login')
def login(
    user: str, password: str, response: Response,
    credentials_user = Depends(get_current_username)
    ):
    
    session_token = sha256(bytes(f"{user}{password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.tokens_list += session_token
    
    response.set_cookie(key="session_token", value=session_token)
    
    response= requests.post('https://pikachupy.herokuapp.com/welcome', allow_redirects=False)
    
    return response
'''
