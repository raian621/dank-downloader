from pytube import YouTube

def on_progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    percent_complete = (total_size - bytes_remaining) / total_size
    print(percent_complete)

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
    return yt.streams.filter(
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

def download_audio(url: str, file_extension=None, file_destination=None):
    pass

def download_video(url: str, file_extension=None, resolution=None, fps=None, file_destination=None):
    streams = get_pytube_streams(url, file_extension=file_extension, resolution=resolution, progressive=True, fps=fps)
    stream = streams.order_by('resolution').desc().first()

    stream.download(file_destination)
