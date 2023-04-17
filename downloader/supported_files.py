DEFAULT_FILE_FORMAT = 'mp4'

additional_file_formats = {
    "video": {
        "mov",
        "avi"
    },
    "audio": {
        "mp3",
        "wav"
    }
}

class UnsupportedFileExtError(Exception):
     """
    Exception raised when an extension is requested that is not supported
    """
     
     def __init__(self, extension):
        self.message = f"UnsupportedFileExtError: '{extension}' format not supported"
        super().__init__(self.message)