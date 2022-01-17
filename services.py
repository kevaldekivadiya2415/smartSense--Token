import database as _database
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas



def create_database():
    return _database.Base.metadata.create_all(bind = _database.engine)


def get_db():
    db = _database.SessionLocal()

    try:
        yield db
    finally:
        db.close()

def create_user(db : _orm.Session , user : _schemas.Token):
    db_user = _models.token(token_id = user.token_id , Number_Of_Item = user.Number_Of_Item , status = user.status , time = user.time)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

