from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from .models import *


engine = create_engine("sqlite+pysqlite:///dank-downloader.db", echo=True)
Base.metadata.create_all(bind=engine)

def get_user(session):
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


def create_playlist(name, description, session):
    user = get_user(session)
    user.playlists.append(Playlist(0, name, description, get_user(session)))
    add_entity(user, session)
    session.commit()

def add_media_to_playlist(playlist, media, session):
    playlist.playlist.append(media)
    add_entity(playlist, session)
