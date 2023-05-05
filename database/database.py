from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

from .models import *


engine = create_engine("sqlite+pysqlite:///dank-downloader.db", echo=False)
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
  if result.count() == 0:
    user = User(username=username)
    session.add(user)
  else:
    user = result.first() 
  return user


def create_playlist(name: str, description: str, session: Session|None=None):
  """
  Creates a new playlist in the database.
  ---------------------------------------------------------------
  
  params:
    name: the name of the playlist
    description: the description of the playlist
    session: SQLAlchemy database session object
  """
  playlist = None
  if session:
    user = get_user(session)
    playlist = Playlist(
      playlength=0, 
      name=name, 
      description=description, 
      user=user,
      user_id=user.id
    )
    user.playlists.append(playlist)
    session.add(user)
    session.commit()
  else:
    with make_session() as _session:
      playlist = create_playlist(name, description, _session)

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
    if (videodata and result.first()):
      result = result.where(
        Media.videodata.fps==videodata.fps,
        Media.videodata.resolution==videodata.resolution
      )
    if (result.first()):
      media_exists = True

  return media_exists

def add_media_to_playlist(mediaID, playlistID):
  with make_session() as session:
    playlist = session.query(Playlist).where(Playlist.id==playlistID).first()
    media = session.query(Media).where(Media.id==mediaID).first()
    if playlist == None or media == None:
      return
    if playlist.media:
      playlist.media.append(media)
    else:
      playlist.media = [media]
    session.commit()

def remove_media_from_playlist(mediaID, playlistID):
  with make_session() as session:
    playlist = session.query(Playlist).where(Playlist.id==playlistID).first()
    media = session.query(Media).where(Media.id==mediaID).first()
    if playlist == None or media == None:
      return
    playlist.media.remove(media)
    session.commit()

def delete_media(mediaID):
  with make_session() as session:
    media = session.query(Media).where(Media.id==mediaID).first()
    if media:
      session.delete(media)
    session.commit()

def delete_playlist(playlistID):
  with make_session() as session:
    playlist = session.query(Playlist).where(Playlist.id==playlistID).first()
    if playlist:
      session.delete(playlist)
    session.commit()