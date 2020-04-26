from fastapi import FastAPI, Response, HTTPException
from hashlib import sha256
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

app = FastAPI()
app.num = 0
app.count = -1
app.users = {"trudnY": "PaC13Nt", "admin": "admin"}
app.secret = "secret"
app.tokens = []
patlist = []


@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/welcome")
def welcome_to_the_jungle():
	return {"message": "Welcome to the jungle! We have funny games!"}


@app.post("/login/")
def login_to_app(user: str, passw: str, response: Response):
	if user in app.users and passw == app.users[user]:
		s_token = sha256(bytes(f"{user}{passw}{app.secret}", encoding='utf8')).hexdigest()
		app.tokens += s_token
		response.set_cookie(key="session_token",value=s_token)
		response = RedirectResponse(url='/welcome')
		print('logged in')
		return response
	else:
		raise HTTPException(status_code=401)
'''
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



@app.post("/login/")
def login(
    user: str, password: str, response: Response,
    credentials_user = Depends(get_current_username)
    ):
    
    session_token = sha256(bytes(f"{user}{password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.tokens_list.append(session_token)
    
    response.set_cookie(key="session_token", value=session_token)
    
        
    response = RedirectResponse(url = 'https://pikachupy.herokuapp.com/welcome')
    response(status_code=status.HTTP_302_FOUND)
    
    return RedirectResponse(url='/welcome')
'''
