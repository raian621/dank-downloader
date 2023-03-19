from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

from .models import *


engine = create_engine("sqlite+pysqlite:///dank-downloader.db", echo=True)
Base.metadata.create_all(bind=engine)

def make_session():
    return sessionmaker(bind=engine)()


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
    playlist = Playlist(0, name, description, get_user(session))
    user.playlists.append(playlist)
    session.add(user)

    return playlist

def media_exists(
    playlength:int,
    extension:str,
    url:str,
    filepath:str,
    title:str,
    subtitle:str,
    videodata:VideoData|None=None
) -> bool :
    Session = sessionmaker(bind=engine)
    media_exists = False
    with Session() as session:
        result = session.query(Media).where(
            Media.playlength==playlength,
            Media.extension==extension,
            Media.url==url,
            Media.filepath==filepath,
            Media.title==title,
            Media.subtitle==subtitle
        )
        print("RESULT:", result)
        if (videodata and result.first()):
            result = result.where(
                Media.videodata.fps==videodata.fps,
                Media.videodata.resolution==videodata.resolution
            )
        if (result.first()):
            media_exists = True

    return media_exists