from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from .models import *


engine = create_engine("sqlite+pysqlite:///dank-downloader.db", echo=True)
Base.metadata.create_all(bind=engine)

def get_user(session):
    Session = sessionmaker(engine)
    username = None

    for var in ("USER", "USERNAME", "LOGNAME"):
        if var in os.environ:
            username = os.environ[var]

    user = None
    result = session.query(User).where(User.username.is_(username))
    print(result)
    if result.count() == 0:
        user = User(username)
        session.add(user)
    else:
        user = result.first()

    return user
    

def add_entity(entity, session):
    session.add(entity)
    session.commit()
