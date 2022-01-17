from xmlrpc.client import Boolean, DateTime
from pydantic import BaseModel
import datetime as _dt
from typing import List

class Token(BaseModel):
    token_id : int
    Number_Of_Item : int
    status : Boolean
    time : _dt.datetime
