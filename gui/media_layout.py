from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea
from .download_window import MediaDownloadWindow
from database import make_session
from database.models import Media, VideoData

class MediaRow(QHBoxLayout):
  def __init__(self, parent=None):
    super().__init__(parent)
    

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
    tableWidget = QWidget()
    self.tableLayout = QVBoxLayout(tableWidget)
    scrollArea.setWidget(tableWidget)
    layout = QVBoxLayout()
    layout.addLayout(barLayout)
    layout.addWidget(scrollArea)
    self.addLayout(layout)


  def showDownloadWindow(self):
    self.dlWindow = MediaDownloadWindow()
    self.dlWindow.show()


  def populateTable(self):
    self.heading = QHBoxLayout()
    self.heading.addWidget(QLabel("TITLE"))
    self.heading.addWidget(QLabel("FORMAT"))
    self.heading.addWidget(QLabel("LENGTH"))
    self.heading.addWidget(QLabel("LOCATION"))
    self.heading.addWidget(QLabel("OPTIONS"))

    self.rows = [self.heading]
    self.getMediaFromDB()

    for row in self.rows:
      print(row)
      self.tableLayout.addLayout(row)


  def getMediaFromDB(self):
    # shit, the layout stuff isn't working
    with make_session() as session:
      mediaList = session.query(Media).all()
      print(mediaList)
      for media in mediaList:
        layout = QHBoxLayout()
        layout.addWidget(QLabel(f'{media.title}, {media.subtitle}'))
        layout.addWidget(QLabel(media.extension))
        layout.addWidget(QLabel(f"{media.playlength}"))
        layout.addWidget(QLabel(media.filepath))
        layout.addWidget(QLabel("options"))
        self.rows.append(layout)
