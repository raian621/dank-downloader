from pytube import YouTube
import moviepy.editor as mp
import ffmpeg
import os
import re

from database import *


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


def get_pytube_streams(
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
):
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

        print(streams)
    except Exception as e:
        print(e)

    return (streams, yt.length)


def download_video(url: str, file_extension=None, resolution=None, fps=None, file_destination=DOWNLOAD_DIRECTORY, register=True, title=None, subtitle=None):
    
    streams, length = get_pytube_streams(url, file_extension=file_extension, progressive=False, fps=fps)

    video_stream = streams.filter(resolution=resolution).desc().first()
    audio_stream = streams.filter(only_audio=True).order_by('bitrate').desc().first()

    print(video_stream)
    print(audio_stream)

    if file_extension == None:
        ext = re.findall("\.(.*)", video_file_path)
        if ext:
            file_extension = ext[0]

    video_file_path = video_stream.download(file_destination)
    audio_file_path = None
    if audio_stream:
        audio_file_path = audio_stream.download(file_destination,
                video_file_path.replace(f".{file_extension}", f"_audio.mp4"))
        video_file_path_old = video_file_path
        # combine video and audio files.
        # I swear this was the only way to get HD video
        video_file_path = video_file_path.replace(f".{file_extension}", f"_video.mp4")
        os.rename(video_file_path_old, video_file_path)
        video = ffmpeg.input(video_file_path)
        audio = ffmpeg.input(audio_file_path)
        ffmpeg.output(video, audio, video_file_path_old).run()
        os.remove(audio_file_path)
        os.remove(video_file_path)

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
            add_entity(user, session)

    return video_file_path


def download_audio(url: str, file_extension="mp4", file_destination=DOWNLOAD_DIRECTORY, register=True, title=None, subtitle=None):
    streams, length = get_pytube_streams(url, file_extension)
    
    file_path = None
    # if there are no audio streams of the specified file_extension, download
    # mp4 file and convert it into a file with the specified file extension
    if streams == None:
        video_file_path = download_video(url, file_extension="mp4", register=False)
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

            add_entity(user, session)

    return file_path

