from pytube import YouTube


def main():
    yt = YouTube('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()


if __name__ == '__main__':
    main()