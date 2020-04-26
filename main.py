from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Response, status
from fastapi import Depends, Cookie, HTTPException
from hashlib import sha256

import secrets


app = FastAPI()
def is_logged(session_token):
	def outer(func):
		@wraps(func)
		def inner(*args,**kwargs):
			if session_token in app.sesions:
				return func(*args,**kwargs)
			else :
				raise  HTTPException(401,f"Your session(Cookie) :{session_token}, logged sessions: {app.sesions}")
		return inner
	return outer
  
@app.post('/welcome')
@app.get("/welcome")
@is_logged(session_token=Cookie(None))
def welcome(request: Request):
	return templates.TemplateResponse("welcome.html", {"request":request, "user" : app.sesions[session_token]})


@app.get('/login') # zeby latwo w przegladarce sie zalogowac
@app.post("/login")
def login( response: Response, credentials: HTTPBasicCredentials = Depends(security)):
	try :
		if credentials.password==app.users[credentials.username]:
			s_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
			response.set_cookie(key="session_token",value=s_token)
			response.status_code=302
			response.headers["Location"]="/welcome"
			app.sesions[s_token]=credentials.username
			return response
		else: 
			raise HTTPException(401,'Incorrect password')
	except KeyError: 
		raise HTTPException(401,"User does not exists")
'''

@app.get("/welcome")
def get_welcome():
	return "Hello!"


app.secret_key = "very constatn and random secret, best 64 characters"
app.tokens_list = []
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



@app.post("/login")
def login(
    user: str, password: str, response: Response,
    credentials_user = Depends(get_current_username)
    ):
    
    session_token = sha256(bytes(f"{user}{password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.tokens_list.append(session_token)
    
    response.set_cookie(key="session_token", value=session_token)
    
    response.status_code = 302
    response.headers["Location"]="/welcome"
    
    return response
'''
