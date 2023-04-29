from downloader.playlist_downloader import *
from downloader.playlist_manager import *

pd = PlaylistDownloader()

print(pd.load_configuration(filepath='example.json'))
pd.download()
