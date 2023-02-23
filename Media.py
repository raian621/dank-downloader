import MediaData

class Media:
    def __init__(self, playback_length: int, media_url: str, filepath: str, media_data: MediaData):
        self.playback_length = playback_length
        self.media_url = media_url
        self.filepath = filepath
        self.media_data = media_data
