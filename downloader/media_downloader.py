from pytube import YouTube
from threading import Thread
import ffmpeg

from .util import *
from .supported_files import *

class MediaDownloader:
  def __init__(self, url):
    self.url = url
    self.yt = YouTube(url)
    self.length = self.yt.length
    self.streams, self.formats, self.bitrates = \
      (None, None, None)


  def get_streams(
      self,
      fps=None,
      res=None,
      resolution=None,
      mime_type=None,
      type=None,
      subtype=None,
      file_extension=None,
      abr=None,
      bitrate=None,
      video_codec=None,
      audio_codec=None,
      only_audio=None,
      only_video=None,
      use_existing=True
  ):
    if use_existing and self.streams:
      return (self.streams, self.length)

    self.yt.register_on_progress_callback(on_progress_callback)

    try:
      self.streams = self.yt.streams.filter(
        fps=fps,
        res=res,
        resolution=resolution,
        mime_type=mime_type,
        type=type,
        subtype=subtype,
        file_extension=file_extension,
        abr=abr,
        bitrate=bitrate,
        video_codec=video_codec,
        audio_codec=audio_codec,
        only_audio=only_audio,
        only_video=only_video,
        adaptive=True
      )
    except Exception as e:
      print(e)

    return (self.streams, self.length)

  def get_resolutions(self):
    if self.streams == None:
      self.get_streams()
    # if the downloader still can't get any streams, return none
    if self.streams == None:
      return None
    
    self.resolutions = set()
    for stream in self.streams:
      if stream.resolution:
        self.resolutions.add(stream.resolution)

    self.resolutions = sorted(list(self.resolutions), key=resolution_to_int, reverse=True)
    
    return self.resolutions


  def get_bitrates(self):
    if self.streams == None:
      self.get_streams()
    # if the downloader still can't get any streams, return none
    if self.streams == None:
      return None

    if self.bitrates == None:
      bitrates = set()
      for stream in self.streams.filter(only_audio=True):
        if stream.bitrate:
          bitrates.add(stream.bitrate)

      self.bitrates = list(bitrates)
      self.bitrates.sort()

    return self.bitrates


  def get_formats(self, is_audio=False):
    if self.streams == None:
      self.get_streams()
    # if the downloader still can't get any streams, return none
    if self.streams == None:
      return None

    if self.formats == None:
      # formats = (is_audio ? asdf['audio'] : asdf ['video'])
      formats = additional_file_formats['audio'] if is_audio else additional_file_formats['video'] 
      for stream in self.streams:
        if stream.subtype:
          formats.add(stream.subtype)

      self.formats = list(formats)
      self.formats.sort()

    return self.formats

  def download_video(
    self,
    file_extension:str="mp4", 
    resolution:str|None=None, 
    fps:float|None=None,
    file_destination:str=DOWNLOAD_DIRECTORY,
  ) -> str:
    """
      Downloads a video with audio from the given url.
      In order to support HD resolution, we have to download video and
      audio streams seperately and then combine them with ffmpeg.
    ---------------------------------------------------------------
    params:
      url: the url to download the media from
      file_extension: the desired file extension for the media
      resolution: the desired video resolution for the media
      fps: the frames per second for the media
      file_destination: the folder in which the media will download
        to
    returns:
      The a dict that contains information necessary to register media
      in the database.
    """
    if self.streams == None:
      self.get_streams()

    # TODO: add code to accept unavailable file types; basically try to
    # just download an available format like mp4 and convert it to the
    # requested file type at the end of the method

    convert_to = None
    if file_extension in additional_file_formats['video']:
      convert_to = file_extension
      file_extension = DEFAULT_FILE_FORMAT

    video_stream = self.streams.filter(only_video=True, resolution=resolution, fps=fps, file_extension=file_extension).desc().first()
    audio_stream = self.streams.filter(only_audio=True, file_extension=file_extension).order_by('bitrate').desc().first()

    # return none early if no streams were found
    if not (video_stream and audio_stream):
      return None

    if resolution == None:
      resolution = video_stream.resolution
    if fps == None:
      fps = video_stream.fps

    title = video_stream.title
    file_path = os.path.join(file_destination, f"{title}_{resolution}_{fps}.{file_extension}")

    # TODO: add sentinel here to avoid redownloading files :wtf

    video_file_path = os.path.join(file_destination, file_path.replace(f".{file_extension}", f"_video.{file_extension}"))
    audio_file_path = os.path.join(file_destination, file_path.replace(f".{file_extension}", f"_audio.{file_extension}"))
    
    video_thread = Thread(
      target=download_stream,
      args=(video_stream, video_file_path,)
    )
    
    # if there was no audio stream, do not try to download the audio file
    audio_thread = Thread(
      target=download_stream, 
      args=(audio_stream, audio_file_path,)
    )

    video_thread.start()
    audio_thread.start()
    video_thread.join()
    audio_thread.join()

    video_exists = os.path.exists(video_file_path)
    audio_exists = os.path.exists(audio_file_path)

    # combine video and audio files.
    # I swear this was the only way to get HD video

    if video_exists and audio_exists:
      video = ffmpeg.input(video_file_path)
      audio = ffmpeg.input(audio_file_path)
      ffmpeg.output(video, audio, file_path).run()

      os.remove(audio_file_path)
      os.remove(video_file_path)
    elif video_exists:
      os.rename(video_file_path, file_path)
    else:
      return None

    if convert_to != None:
      # video.mp4 -> video.wav
      new_file_path = file_path.replace(f'.{file_extension}', f'.{convert_to}')
      ffmpeg.input(file_path).output(new_file_path).run()
      os.remove(file_path)
      file_extension = convert_to
      file_path = new_file_path

    return {
      "playlength": self.length,
      "extension": file_extension,
      "url": self.url,
      "filepath": file_path,
      "resolution": resolution,
      "fps": fps
    }


  def download_audio(self,
    file_extension:str="mp4", 
    file_destination:str=DOWNLOAD_DIRECTORY,
  ) -> str:
    """
    Downloads audio to file_destination.
    ---------------------------------------------------------------
    params:
      file_extension: the desired file extension for the media
      file_destination: the folder in which the media will download
        to
    returns:
      The a dict that contains information necessary to register media
      in the database.
    """

    # TODO: add code to accept supported, but unavailable file types; 
    # basically try to just download an available format like mp4 
    # and convert it to the requested file type at the end of the method

    convert_to = None
    if file_extension in additional_file_formats['audio']:
      convert_to = file_extension
      file_extension = DEFAULT_FILE_FORMAT

    if self.streams == None:
      self.get_streams
    
    stream = self.streams.filter(only_audio=True, file_extension=file_extension).order_by("bitrate").desc().first()
    if stream == None:
      return None
    
    file_path = os.path.join(file_destination, f"{stream.title}_{stream.bitrate}.{file_extension}")
    download_stream(stream, file_path)

    if convert_to != None:
      # video.mp4 -> video.wav
      new_file_path = file_path.replace(f'.{file_extension}', f'.{convert_to}')
      ffmpeg.input(file_path).output(new_file_path).run()
      os.remove(file_path)
      file_extension = convert_to
      file_path = new_file_path

    return {
      "playlength": self.length,
      "extension": file_extension,
      "url": self.url,
      "filepath": file_path,
      "audiodata": {
        "bitrate": stream.bitrate
      }
    }

