from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea
from .download_window import MediaDownloadWindow
from database import make_session
from database.models import Media


class MediaTable(QScrollArea):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.rows = None
    self.populateTable()


  def populateTable(self):
    widget = QWidget()
    widget.setLayout(QGridLayout())
    self.heading = ['TITLE', 'FORMAT', 'LENGTH', 'LOCATION', 'OPTIONS']
    
    if self.rows == None:
      self.rows = []
      self.getMediaFromDB()

    for i in range(len(self.heading)):
      widget.layout().addWidget(QLabel(self.heading[i]), 0, i + 1)

    for i in range(len(self.rows)):
      widget.layout().addWidget(QPushButton('Play'), i + 1, 0)
      for j in range(len(self.rows[i])):
        if j == 0:
          widget.layout().addWidget(QLabel(self.rows[i][j][0]), i + 1, j + 1)
        else:
          widget.layout().addWidget(QLabel(self.rows[i][j]), i + 1, j + 1)

    self.setWidget(widget)


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
    self.mediaTable = MediaTable()
    layout = QVBoxLayout()
    layout.addLayout(barLayout)
    layout.addWidget(self.mediaTable)
    self.addLayout(layout)


  def showDownloadWindow(self):
    self.dlWindow = MediaDownloadWindow()
    self.dlWindow.repopulateTable = self.mediaTable.populateTable
    self.dlWindow.rows = self.mediaTable.rows
    self.dlWindow.show()