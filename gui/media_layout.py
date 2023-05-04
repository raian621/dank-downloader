from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QMenu
from .download_window import MediaDownloadWindow
from database import make_session
from database.models import Media
from .media_player import MediaPlayer


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
      button = QPushButton('Play')
      button.clicked.connect(lambda: self.createMediaWindow([self.rows[i][3]]))

      widget.layout().addWidget(button, i + 1, 0)
      n_variables = len(self.rows[i])
      for j in range(n_variables):
        if j == 0:
          widget.layout().addWidget(QLabel(self.rows[i][j][0]), i + 1, j + 1)
        else:
          widget.layout().addWidget(QLabel(self.rows[i][j]), i + 1, j + 1)
      self.contextMenu = QMenu()
      self.contextMenu.addAction('Delete', lambda: print(f'Delete {self.rows[i][0][0]}'))
      self.contextMenu.addAction('Add to Playlist', lambda: print('Add to Playlist'))
      contextButton = QPushButton('Options')
      contextButton.setMenu(self.contextMenu)
      widget.layout().addWidget(contextButton, i + 1, n_variables + 1)

    self.setWidget(widget)

  def createMediaWindow(self, mediaList):
    self.mediaPlayer = MediaPlayer(mediaList)
    self.mediaPlayer.show()

  def getMediaFromDB(self):
    with make_session() as session:
      mediaList = session.query(Media).all()
      for media in mediaList:
        row = [
          [f'{media.title}', f'{media.subtitle}'],
          media.extension,
          f"{media.playlength}",
          media.filepath,
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