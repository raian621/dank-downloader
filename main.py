from downloader import download_video, download_audio
from database import *

def main():
    download_audio('https://www.youtube.com/watch?v=dQw4w9WgXcQ', file_extension="wav")

if __name__ == '__main__':
    main()