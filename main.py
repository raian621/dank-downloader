from downloader import download_video, download_audio

def main():
    url = input("Please enter a video URL from YouTube: ")
    is_audio = input("Audio download [A] or video download [V]: ").upper() == "A"
    audio_extensions = ["mp3", "wav"]
    video_extensions = ["mp4"]

    extensions = audio_extensions if is_audio else video_extensions
    for i in range(len(extensions)):
        print(f"({i + 1}) {extensions[i]}")

    extension = extensions[int(input("Please select an extension: ")) - 1]
    
    download_audio(url, extension) if is_audio else download_video(url, extension)
    

if __name__ == '__main__':
    main()