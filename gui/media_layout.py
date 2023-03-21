from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea
from .download_window import MediaDownloadWindow
# class MediaListLayout(QScrollArea):
#   def __init__(self, parent=None):

  
class MediaLayout(QVBoxLayout):
  def __init__(self, parent=None):
    super().__init__(parent)

    downloadButton = QPushButton("Download")
    downloadButton.clicked.connect(self.showDownloadWindow)
    label = QLabel("MEDIA")
    barLayout = QHBoxLayout()
    barLayout.addWidget(label)
    barLayout.addWidget(downloadButton)
    self.addLayout(barLayout)

  def showDownloadWindow(self):
    self.dlWindow = MediaDownloadWindow()
    self.dlWindow.show()
