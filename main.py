from downloader import download_video, download_audio

def main():
    download_video('https://www.youtube.com/shorts/tv2kXFrXucQ', file_extension="mp4")

if __name__ == '__main__':
    main()