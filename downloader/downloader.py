from pytube import YouTube
import moviepy.editor as mp
import os

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
    except Exception as e:
        print(e.with_traceback)

    return streams

def download_audio(url: str, file_extension=None, file_destination=DOWNLOAD_DIRECTORY):
    streams = get_pytube_streams(url, file_extension)
    
    # if there are no audio streams of the specified file_extension, download
    # mp4 file and convert it into a file with the specified file extension
    if streams == None:
        video_file_path = download_video(url, file_extension="mp4")
        video = mp.VideoFileClip(video_file_path)
        video.audio.write_audiofile(video_file_path.replace("mp4", file_extension))
        os.remove(video_file_path)
        return
    
    streams.download(file_destination)

def download_video(url: str, file_extension=None, resolution=None, fps=None, file_destination=DOWNLOAD_DIRECTORY):
    streams = get_pytube_streams(url, file_extension=file_extension, resolution=resolution, progressive=True, fps=fps)
    stream = streams.order_by('resolution').desc().first()
    print(DOWNLOAD_DIRECTORY)
    return stream.download(file_destination)
