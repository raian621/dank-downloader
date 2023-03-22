from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea
from .download_window import MediaDownloadWindow
from database import make_session
from database.models import Media, VideoData


class MediaTable(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setLayout(QGridLayout())
    self.populateTable()


  def populateTable(self):
    self.heading = QHBoxLayout()
    self.heading = ['TITLE', 'FORMAT', 'LENGTH', 'LOCATION', 'OPTIONS']
    self.rows = []
    self.getMediaFromDB()
    for i in range(len(self.heading)):
      self.layout().addWidget(QLabel(self.heading[i]), 0, i + 1)

    for i in range(len(self.rows)):
      self.layout().addWidget(QPushButton('Play'), i + 1, 0)
      for j in range(len(self.rows[i])):
        if j == 0:
          self.layout().addWidget(QLabel(self.rows[i][j][0]), i + 1, j + 1)
        else:
          self.layout().addWidget(QLabel(self.rows[i][j]), i + 1, j + 1)


  def getMediaFromDB(self):
    with make_session() as session:
      mediaList = session.query(Media).all()
      print(mediaList)
      for media in mediaList:
        row = [
          [f'{media.title}', f'{media.subtitle}'],
          media.extension,
          f"{media.playlength}",
          media.filepath,
          "options"
        ]

        self.rows.append(row)


class MediaLayout(QVBoxLayout):
  def __init__(self, parent=None):
    super().__init__(parent)

    downloadButton = QPushButton("Download")
    downloadButton.clicked.connect(self.showDownloadWindow)
    label = QLabel("MEDIA")
    barLayout = QHBoxLayout()
    barLayout.addWidget(label)
    barLayout.addWidget(downloadButton)
    scrollArea = QScrollArea()
    scrollArea.setWidget(MediaTable())
    layout = QVBoxLayout()
    layout.addLayout(barLayout)
    layout.addWidget(scrollArea)
    self.addLayout(layout)


  def showDownloadWindow(self):
    self.dlWindow = MediaDownloadWindow()
    self.dlWindow.show()