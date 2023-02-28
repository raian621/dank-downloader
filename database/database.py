from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from .models import *


engine = create_engine("sqlite+pysqlite:///dank-downloader.db", echo=True)
Base.metadata.create_all(bind=engine)

def get_user():
    Session = sessionmaker(engine)
    username = None

    for var in ("USER", "USERNAME", "LOGNAME"):
        if var in os.environ:
            username = os.environ[var]

    user = None
    with Session() as session:
        result = session.query(User).where(User.username.is_(username))
        print(result)
        if result.count() == 0:
            user = User(username)
            session.add(user)
        else:
            user = result.first()
        session.expunge_all()

    return user
    

def add_entity(entity):
    Session = sessionmaker(engine)

    with Session() as session:
        session.add(entity)
        session.commit()
