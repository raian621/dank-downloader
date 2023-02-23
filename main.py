from pytube import YouTube
yt = YouTube('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()