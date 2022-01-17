from typing import List
from fastapi import FastAPI
import services as _services
import schemas as _schemas
import sqlalchemy.orm as _orm
from fastapi import Depends
from fastapi import HTTPException

app  = FastAPI()

_services.create_database()

@app.get("/")
def Home():
    return {"Hello" : "Welcome to Token management system"}

@app.post("/Users/" , response_model= _schemas.Token)
def create_token(token : _schemas.Token , db : _orm.Session = Depends(_services.get_db)):
    '''db_user = _services.create_user(db = db , token_id = token.token_id , Number_Of_Item = token.Number_Of_Item , status = token.status  , time = token.time)
    if token.status:
        raise HTTPException(status_code=400 , detail="Woops token is not free" ) 
    
    return _services.token(db = db , token = token) '''
    return token

