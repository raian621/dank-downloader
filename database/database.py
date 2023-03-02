from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

from .models import *


engine = create_engine("sqlite+pysqlite:///dank-downloader.db", echo=True)
Base.metadata.create_all(bind=engine)

def get_user(session: Session) -> User:
    """
    Gets a User object for the current user from database.
    If the user does not exist in the database, the user is created
    and a User object is returned.
    ---------------------------------------------------------------

    params:
        session: SQLAlchemy database session object
    
    returns:
        a User object
    """

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
    

def add_entity(entity: Base, session: Session):
    """
    Adds an object to the database or updates an object in the
    database
    ---------------------------------------------------------------

    params:
        entity: the object to be added to the database
        session: SQLAlchemy database session object
    """
    
    session.add(entity)
    session.commit()


def create_playlist(name: str, description: str, session: Session):
    """
    Creates a new playlist in the database.
    ---------------------------------------------------------------
    
    params:
        name: the name of the playlist
        description: the description of the playlist
        session: SQLAlchemy database session object
    """

    user = get_user(session)
    user.playlists.append(Playlist(0, name, description, get_user(session)))
    add_entity(user, session)
    session.commit()

def add_media_to_playlist(playlist: Playlist, media: Media, session: Session):
    """
    Adds a Media object to a Playlist in the database.
    ---------------------------------------------------------------
    
    params:
        playlist: the Playlist object to add the media to
        media: the Media object to add to the playlist
        session: SQLAlchemy database session object
    """

    playlist.playlist.append(media)
    add_entity(playlist, session)
