#Database tables

import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt

import database as _database

class token(_database.Base):
    __tablename__ = 'token'
    token_id = _sql.Column(_sql.Integer , primary_key= True , index= True)
    Number_Of_Item = _sql.Column(_sql.Integer , index= True)
    status = _sql.Column(_sql.Boolean , default= True)
    time = _sql.Column(_sql.DateTime , default= _dt.datetime.now() )