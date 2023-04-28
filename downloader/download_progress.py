class Progress:
  def __init__(self):
    self.value = 0.0


class DownloadProgressTracker:
  def __init__(self):
    self.progress = Progress()

  def progress_callback(self, stream, chunk, bytes_remaining):
    total_size = stream.filesize
    self.progress.value = (total_size - bytes_remaining) / total_size