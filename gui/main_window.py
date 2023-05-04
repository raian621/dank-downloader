from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMainWindow, QApplication
from PySide6.QtGui import QIcon
from .playlist_layout import PlaylistLayout
from .media_layout import MediaLayout
from .playlist_view import PlaylistView
from downloader import is_mock_mode
from .error_window import ErrorWindow

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
    self.resize(800, 500)
    if is_mock_mode():
      self.setWindowTitle('Dank Downloader [MOCK MODE]')
    else:
      self.setWindowTitle('Dank Downloader')
    self.setWindowIcon(QIcon('assets/dankdownloader.ico'))
    self.showMediaView()

  def showMediaView(self):
    try:
      self.mediaView = MediaView(showPlaylistView=self.showPlaylistView)
      self.setCentralWidget(self.mediaView)
    except Exception as e:
      print(e)

  def showPlaylistView(self, title):
    print(title)
    self.playlistView = PlaylistView(title=title, goBack=self.showMediaView)
    self.setCentralWidget(self.playlistView)

  def showErrorWindow(self, exc_type, exc_value):
    self.errorWindow = ErrorWindow(None, str(exc_value), str(exc_type))
    self.errorWindow.show()


  def excepthook(self, exc_type, exc_value, exc_tb):
    self.showErrorWindow(exc_type, exc_value)