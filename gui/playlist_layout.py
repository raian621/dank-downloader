from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

class PlaylistListLayout(QVBoxLayout):
  def __init__(self, parent=None):
    super().init()
  
class PlaylistLayout(QVBoxLayout):
  def __init__(self, parent=None):
    super().__init__(parent)

    downloadButton = QPushButton("Download")
    downloadButton.clicked.connect(lambda: showDownloadWindow(False))
    addButton = QPushButton("Add")
    label = QLabel("PLAYLISTS")
    barLayout = QHBoxLayout()
    barLayout.addWidget(label)
    barLayout.addWidget(downloadButton)
    barLayout.addWidget(addButton)
    self.addLayout(barLayout)

def showDownloadWindow(is_media:bool):
  print("SHOW MEDIA DOWNLOAD BUTTON") if is_media else print("SHOW PLAYLIST DOWNLOAD BUTTON")
