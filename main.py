from downloader import download_media

def main():

    download_media('https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        progressive=True,
        file_extension="mp4"
    )

if __name__ == '__main__':
    main()