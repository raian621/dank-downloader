from .media_downloader import MediaDownloader
from .util import DOWNLOAD_DIRECTORY, create_media_hash, add_media_to_db
from database import make_session, get_user
import os

class MediaManager(MediaDownloader):
  def __init__(self, url):
    super().__init__(url)
  

  def download_video(
      self,
      file_extension:str="mp4",
      resolution:str|None=None,
      fps:float|None=None,
      file_destination:str=DOWNLOAD_DIRECTORY,
      title:str|None=None,
      subtitle:str|None=""
  ):
    result = super().download_video(
      file_extension=file_extension,
      resolution=resolution,
      fps=fps,
      file_destination=file_destination
    )

    if title == None:
      title = self.yt.title

    result["title"] = title
    result["subtitle"] = subtitle

    if result:
      print(add_media_to_db(result, is_video=True))
    return result

  
  def download_audio(
      self,
      file_extension:str="mp4",
      file_destination:str=DOWNLOAD_DIRECTORY,
      title:str|None=None,
      subtitle:str|None=""
  ):
    result = super().download_audio(
      file_extension=file_extension,
      file_destination=file_destination
    )

    if title == None: 
      title = self.yt.title

    result["title"] = title
    result["subtitle"] = subtitle

    if result:
      print(add_media_to_db(result, is_video=False))

    return result
