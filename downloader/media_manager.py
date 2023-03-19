from .media_downloader import MediaDownloader
from .util import DOWNLOAD_DIRECTORY 

class MediaManager(MediaDownloader):
  def __init__(self, url):
    super().__init__(url)
  

  def download_video(
      self,
      file_extension:str="mp4",
      resolution:str|None=None,
      fps:float|None=None,
      file_destination:str=DOWNLOAD_DIRECTORY,
      title:str|None="New Media",
      subtitle:str|None="Subtitle"
  ):
    super().download_video(
      file_extension=file_extension,
      resolution=resolution,
      fps=fps,
      file_destination=file_destination
    )

  
  def download_audio(
      self,
      file_extension:str="mp4",
      file_destination:str=DOWNLOAD_DIRECTORY,
      title:str|None="New Media",
      subtitle:str|None="Subtitle"
  ):
    super().download_audio(
      file_extension=file_extension,
      file_destination=file_destination
    )
