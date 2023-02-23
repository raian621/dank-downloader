from pytube import YouTube

def download_media(url: str,
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
    stream = yt.streams\
        .filter(
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
        )\
        .order_by('resolution')\
        .desc()\
        .first()

    stream.download()
