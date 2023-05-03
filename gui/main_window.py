from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMainWindow
from .playlist_layout import PlaylistLayout
from .media_layout import MediaLayout

class MediaView(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)

    playlistLayout = PlaylistLayout()
    mediaLayout = MediaLayout()

    layout = QVBoxLayout()
    layout.addLayout(playlistLayout)
    layout.addLayout(mediaLayout)
    self.setLayout(layout)


class MainWindow(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.resize(800, 500)
    self.showMediaView()


  def showMediaView(self):
    self.mediaView = MediaView()
    self.setCentralWidget(self.mediaView)

