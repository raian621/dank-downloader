from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMainWindow
from .playlist_layout import PlaylistLayout
from .media_layout import MediaLayout

class MainWindow(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    
    playlistLayout = PlaylistLayout()
    mediaLayout = MediaLayout()

    layout = QVBoxLayout()
    layout.addLayout(playlistLayout)
    layout.addLayout(mediaLayout)
    widget = QWidget()
    widget.setLayout(layout)

    self.setCentralWidget(widget)
    self.resize(800, 500)

  def closeEvent(self, event):
    print("sdfihjjkfhjgfhkdh")