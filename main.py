from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Response, status
from fastapi import Depends, Cookie, HTTPException
from hashlib import sha256

import secrets
import requests

app = FastAPI()

@app.get('/welcome')
def get_welcome():
	return  {"message": "Welcome"}


app.secret_key = "very constatn and random secret, best 64 characters"
app.tokens = []



from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route
import base64
import binascii


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return AuthenticationError('auto not in')

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return AuthenticationError('Invalid basic')
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        if username == "admin" and password == "admin":
        	return AuthCredentials(["authenticated"]), SimpleUser(username)

@app.post("/login/")
def create_cookie(user: str, password: str, response: Response):
	if request.user.is_authenticated:
   		session_token = sha256(bytes(f"{user}{password}{app.secret_key}")).hexdigest()
		app.tokens+=session_token
		response = RedirectResponse(url='/welcome')
    		response.set_cookie(key="session_token", value=session_token)
		response.status_code=302
    		return response
	else:
		raise AuthenticationError('Invalid basic auth credentials')
		

@app.get("/data/")
def create_cookie(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.tokens :
        raise HTTPException(status_code=403, detail="Unathorised")
    response.set_cookie(key="session_token", value=session_token)
'''
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
