from downloader import download_video, download_audio
from downloader.supported_files import supported_file_formats as sff
from gui import create_main_window

def main():
    # create_main_window()

    
    url = input("Please enter a video URL from YouTube: ")
    is_audio = input("Audio download [A] or video download [V]: ").upper() == "A"
    audio_extensions = [*sff['audio'], 'no preference']
    video_extensions = [*sff['video'], "no preference"]

    extensions = audio_extensions if is_audio else video_extensions
    for i in range(len(extensions)):
        print(f"({i + 1}) {extensions[i]}")

    extension = extensions[int(input("Please select an extension: ")) - 1]
    if extension == "no preference":
        extension = None

    resolution = None
    if not is_audio:
        resolution = input("Enter desired resolution (leave blank to automatically choose best resolution): ")
        if len(resolution) == 0:
            resolution = None

    download_audio(url, extension) if is_audio else download_video(url, extension, resolution=resolution)
    
if __name__ == '__main__':
    main()