from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import databases
import sqlalchemy
from sqlalchemy import *

SQLALCHEMY_DATABASE_URL = "sqlite:///./token.db"

metadata_obj = MetaData()
db = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Database table
token = sqlalchemy.Table(
    "token", metadata_obj,
    Column("token_id", Integer, primary_key=True),
    Column("number_of_item", Integer),
    Column("status", Boolean, default=True),
    Column("time", Float, nullable=False)
)
metadata_obj.create_all(engine)

#pydantic models
class Token(BaseModel):
    token_id: int
    number_of_item: int
    status: bool
    time: float

class Token_2(BaseModel):
    number_of_item: int
    status: bool
    time: float

class update_number_of_item(BaseModel):
    number_of_item: int
    time: float

async def start():
    for i in range(1, 101):
        query = token.insert().values(
            token_id = i,
            number_of_item = 0,
            status = False,
            time = 0.0
        )
        await db.execute(query)

app = FastAPI(title='Token System')


@app.get('/')
async def home():
    await start()
    return {"Hello" : "Welcome to token management system"}


@app.get('/list all token')
async def list_all_token():
    query = "select * from token"
    user = await db.fetch_all(query)
    return user

@app.get("/token details")
async def get_active_token():
    query = "select token_id from token where status = True"
    user = await db.fetch_all(query)
    return user

@app.get("/User by token ID/{token_id}")
async def get_by_token_id(token_id: int):
    user_details = await db.fetch_one("SELECT * FROM token WHERE token_id =" + str(token_id))
    if user_details is None:
        raise HTTPException(status_code=404, detail="Data is not found")
    return user_details

@app.post('/Create_token')
async def create_token(t : Token_2):
    token_id = await db.fetch_one("select min(token_id) from token where status = 0 LIMIT 1")
    if token_id[0] == 0:
        raise HTTPException(status_code=404, detail="No Space is available")
    else:
        token_id = int(token_id[0])
        query = token.update().where(token.c.token_id == int(token_id)).values(number_of_item=t.number_of_item, status=t.status, time=t.time)
        #await db.execute("update token set number_of_item=number_of_item , status=True ,time=time where token.token_id == token_id")
        await db.execute(query)
        data = await get_by_token_id(token_id)
        return data


@app.delete('/Using Token_id{tokne_id}')
async def delete_by_id(token_id: int):
    query = token.update().values(number_of_item=0, status=False, time = 0).where(token.c.token_id == token_id)
    if await db.execute(query) > 0:
        return {"Message": "Successfully deleted"}
    else:
        raise HTTPException(status_code=404, detail="Data Not found")


@app.put('/Update number_of_item/{token_id}')
async def update_number_of_item(token_id: int, t: update_number_of_item):
    query = token.update().values(number_of_item=t.number_of_item,time= t.time).where(token.c.token_id == token_id)
    await db.execute(query)
    return await get_by_token_id(token_id)