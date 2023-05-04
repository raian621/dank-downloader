from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMainWindow
from PySide6.QtGui import QIcon
from .playlist_layout import PlaylistLayout
from .media_layout import MediaLayout
from .playlist_view import PlaylistView

class MediaView(QWidget):
  def __init__(self, parent=None, showPlaylistView=None):
    super().__init__(parent)

    playlistLayout = PlaylistLayout(showPlaylistView=showPlaylistView)
    mediaLayout = MediaLayout()

    layout = QVBoxLayout()
    layout.addLayout(playlistLayout)
    layout.addLayout(mediaLayout)
    self.setLayout(layout)


class MainWindow(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.mediaView = None
    self.playlistView = None
    self.resize(800, 500)
    self.setWindowTitle('Dank Downloader')
    self.setWindowIcon(QIcon('assets/dankdownloader.ico'))
    self.showMediaView()

  def showMediaView(self):
    if self.mediaView == None:
      self.mediaView = MediaView(showPlaylistView=self.showPlaylistView)
    self.setCentralWidget(self.mediaView)

  def showPlaylistView(self, title):
    if self.playlistView == None:
      self.playlistView = PlaylistView(title=title)
    self.setCentralWidget(self.playlistView)
