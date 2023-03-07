from pytube import YouTube
import moviepy.editor as mp
import ffmpeg
import os
import re
from threading import Thread

from database import *
from downloader.configuration import ConfigValMissingError, check_configuration
from downloader.supported_files import *

# initialize the default download directory
DOWNLOAD_DIRECTORY = os.path.join(os.path.expanduser('~'), "dank-downloader")
print(DOWNLOAD_DIRECTORY)
if os.path.exists(DOWNLOAD_DIRECTORY) == False:
    os.makedirs(DOWNLOAD_DIRECTORY)


def on_progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    percent_complete = (total_size - bytes_remaining) / total_size
    progress_line_end = "\r" if percent_complete < 1 else "\n"
    print("Download {:.2f}% complete".format(percent_complete * 100), end=progress_line_end)

def download_stream(stream, file_path):
    """
    Downloads a stream to the given file path.

    Used as a target for threads.
    ---------------------------------------------------------------
    
    params:
        stream: the stream to download
        file_path: the path to save the media at.
    """
    try:
        stream.download(filename=file_path)
    except Exception as e:
        print(e)

def resolution_to_int(res):
    num = re.findall('([0-9]+)', res)[0]
    return int(num)

class Downloader:
    def __init__(self):
        self.streams = None
        self.resolutions = None
        self.bitrates = None
        self.formats = None
        self.length = None


    def get_resolutions(self):
        if self.streams == None:
            return None
        
        if self.resolutions == None:
            resolutions = set()
            for stream in self.streams:
                if stream.resolution:
                    resolutions.add(stream.resolution)
            
            self.resolutions = list(resolutions)
            self.resolutions.sort(reverse=True, key=resolution_to_int)
        
        return self.resolutions


    def get_bitrates(self):
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
        

    def get_formats(self):
        if self.streams == None:
            return None
        
        if self.formats == None:
            formats = set()
            for stream in self.streams:
                if stream.subtype:
                    formats.add(stream.subtype)
            
            self.formats = list(formats)
            self.formats.sort()
        
        return self.formats


    def get_streams(
        self,
        url: str,
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
        progressive=None,
        adaptive=None,
        is_dash=None,
        save_results=True,
        use_existing=True
    ):
        if use_existing and self.streams:
            return self.streams
        
        yt = YouTube(url)
        yt.register_on_progress_callback(on_progress_callback)
        streams = None

        try:
            streams = yt.streams.filter(
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
                progressive=progressive,
                adaptive=adaptive,
                is_dash=is_dash
            )
        except Exception as e:
            print(e)

        if save_results:
            self.bitrates = None
            self.resolutions = None
            self.formats = None
            self.streams = streams
            self.length = yt.length

        return (streams, yt.length)


    def download_video(
            self,
            url: str, 
            file_extension:str|None=None, 
            resolution:str|None=None, 
            fps:float|None=None,
            file_destination:str=DOWNLOAD_DIRECTORY,
            register:bool=True,
            title:str|None=None,
            subtitle:str|None=None,
            save_results:bool=False
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
            register: if True, the media is registered in the database, 
                if False, the media is not registered in the database
            title: the title to register the media as in the database
            subtitle: the subtitle to register the media as in the 
                database
        returns:
            The path to the downloaded media
        """

        streams, length = self.get_streams(url, file_extension=file_extension, save_results=save_results, use_existing=True)

        video_stream = streams.filter(only_video=True, resolution=resolution, fps=fps, file_extension=file_extension).desc().first()
        audio_stream = streams.filter(only_audio=True, file_extension=file_extension).order_by('bitrate').desc().first()

        if file_extension == None:
            ext = re.findall("\.(.*)", video_file_path)
            if ext:
                file_extension = ext[0]
        
        title = video_stream.title
        file_path = os.path.join(file_destination, f"{title}.{file_extension}")

        if audio_stream:
            video_file_path = os.path.join(file_destination, f"{title}_video.{file_extension}")
            audio_file_path = os.path.join(file_destination, f"{title}_audio.{file_extension}")

            video_thread = Thread(
                target=download_stream, 
                args=(video_stream, video_file_path,)
            )
            audio_thread = Thread(
                target=download_stream, 
                args=(audio_stream, audio_file_path,)
            )

            video_thread.start()
            audio_thread.start()
            video_thread.join()
            audio_thread.join()

            if not os.path.isfile(video_file_path) or not os.path.isfile(audio_file_path):
                return None

            # combine video and audio files.
            # I swear this was the only way to get HD video
            video = ffmpeg.input(video_file_path)
            audio = ffmpeg.input(audio_file_path)
            ffmpeg.output(video, audio, file_path).run()

            os.remove(audio_file_path)
            os.remove(video_file_path)
        else:
            download_stream(video_stream, file_path)
        
        if register:
            Session = sessionmaker(engine)
            with Session() as session:
                user = get_user(session)
                
                if title == None:
                    title = "New Media"
                if subtitle == None:
                    subtitle = "New Media"

                media = Media(length, file_extension, url, video_file_path, title, subtitle, user)
                videodata = VideoData(video_stream.resolution, video_stream.fps, media)
                media.videodata = videodata
                user.media.append(media)
                session.add(user)
                session.commit()

        return video_file_path


    def download_audio(self,
            url: str, 
            file_extension:str="mp3", 
            file_destination:str=DOWNLOAD_DIRECTORY,
            register:bool=True,
            title:str|None=None,
            subtitle:str|None=None
    ) -> str:
        """
        Downloads audio from the given url.
        ---------------------------------------------------------------

        params:
            url: the url to download the media from
            file_extension: the desired file extension for the media
            file_destination: the folder in which the media will download
                to
            register: if True, the media is registered in the database, 
                if False, the media is not registered in the database
            title: the title to register the media as in the database
            subtitle: the subtitle to register the media as in the 
                database
        returns:
            The path to the downloaded media
        """

        streams, length = self.get_streams(url, file_extension)
        
        file_path = None
        # if there are no audio streams of the specified file_extension, download
        # mp4 file and convert it into a file with the specified file extension
        if streams == None:
            downloader = Downloader()
            video_file_path = downloader.download_video(url, file_extension="mp4", register=False)
            video = mp.VideoFileClip(video_file_path)
            file_path = video_file_path.replace("mp4", file_extension)
            video.audio.write_audiofile(video_file_path.replace("mp4", file_extension))
            os.remove(video_file_path)
        else:
            file_path = streams.first().download(file_destination)

        if register:
            Session = sessionmaker(engine)
            with Session() as session:
                user = get_user(session)
                
                if title == None:
                    title = "New Media"
                if subtitle == None:
                    subtitle = "New Media"
                    
                media = Media(length, file_extension, url, video_file_path, title, subtitle, user)
                user.media.append(media)

                session.add(user)
                session.commit()

        return file_path

    def download_playlist(
            configuration:dict
    ):
        try:
            check_configuration(configuration)
        except (ConfigValMissingError, UnsupportedFileExtError) as e:
            print(e)
            return

        Session = sessionmaker(bind=engine)
        with Session() as session:
            playlist = create_playlist(
                name=configuration['playlistTitle'], 
                description=configuration['playlistDescription'],
                session=session
            )
            for media in configuration['playlistMedia']:
                if media['fileExtension'] in supported_file_formats['video']:
                    downloader = Downloader()
                    downloader.download_video(
                        url=media['url'],
                        file_extension=media['fileExtension'],
                        resolution=media['videoData']['resolution'], 
                        fps=media['videoData']['fps'],
                        title=media['mediaTitle'],
                        subtitle=media['mediaSubtitle']
                    )
                elif media['fileExtension'] in supported_file_formats['audio']:
                    downloader = Downloader()
                    downloader.download_audio(
                        url=media['url'],
                        file_extension=media['fileExtension'],
                        title=media['mediaTitle'],
                        subtitle=media['mediaSubtitle']
                    )

                media_obj = session.query(Media).where(
                    extension=media['fileExtension'],
                    url=media['url'],
                    title=media['title'],
                    subtitle=media['subtitle']
                )

                playlist.media.append(media_obj)
            
            session.add(playlist)
            session.commit()
