from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QMenu
from .download_window import MediaDownloadWindow
from database import make_session
from database.models import Media, Playlist
from .media_player import MediaPlayer
from .add_media_to_playlist_window import AddMediaToPlaylistWindow

class MediaTable(QScrollArea):
  def __init__(self, playlistID=None, parent=None):
    super().__init__(parent)
    self.rows = None
    self.contextMenus = []
    self.mediaIDs = []
    self.populateTable(playlistID)

  def populateTable(self, playlistID=None):
    widget = QWidget()
    widget.setLayout(QGridLayout())
    self.heading = ['TITLE', 'FORMAT', 'LENGTH', 'LOCATION', 'OPTIONS']
    
    if self.rows == None:
      self.rows = []
      print('populateTable() PLAYLIST ID:', playlistID)
      self.getMediaFromDB(playlistID)

    for i in range(len(self.heading)):
      widget.layout().addWidget(QLabel(self.heading[i]), 0, i + 1)

    for i in range(len(self.rows)):
      button = QPushButton('Play')
      # button.clicked.connect passes a bool to the first parameter of the passed function
      # we have to "sacrifice" a placeholder variable _
      button.clicked.connect(lambda _='', filepath=self.rows[i][3]: self.createMediaWindow([filepath]))

      widget.layout().addWidget(button, i + 1, 0)
      n_variables = len(self.rows[i])
      for j in range(n_variables):
        if j == 0:
          widget.layout().addWidget(QLabel(self.rows[i][j][0]), i + 1, j + 1)
        else:
          widget.layout().addWidget(QLabel(self.rows[i][j]), i + 1, j + 1)
      contextMenu = QMenu()
      self.contextMenus.append(contextMenu)
      contextMenu.addAction('Delete', lambda toDelete=self.rows[i][0][0]: print(f'Delete {toDelete}'))
      if i == len(self.mediaIDs):
        mediaID = 0
        with make_session() as session:
          media = session.query(Media).where(Media.title==self.rows[i][0][0]).first()
          mediaID = media.id
        self.mediaIDs.append(mediaID)
      contextMenu.addAction('Add to Playlist', lambda _='', id=self.mediaIDs[i]: self.showAddMediaToPlaylistWindow(id))
      contextButton = QPushButton('Options')
      contextButton.setMenu(contextMenu)
      widget.layout().addWidget(contextButton, i + 1, n_variables + 1)

    self.setWidget(widget)

  def createMediaWindow(self, mediaList):
    self.mediaPlayer = MediaPlayer(mediaList)
    self.mediaPlayer.show()

  def getMediaFromDB(self, playlistID=None):
    print('getMediaFromDB() PLAYLIST ID:', playlistID)
    with make_session() as session:   
      mediaList = None
      if playlistID:
        mediaList = session.query(Playlist).where(Playlist.id==playlistID).first().media
      else:   
        mediaList = session.query(Media).all()
      if mediaList == None:
        mediaList = []
      for media in mediaList:
        row = [
          [f'{media.title}', f'{media.subtitle}'],
          media.extension,
          f"{media.playlength}",
          media.filepath,
        ]
        self.mediaIDs.append(media.id)
        self.rows.append(row)

  def showAddMediaToPlaylistWindow(self, mediaID):
    self.ampWindow = AddMediaToPlaylistWindow(mediaID)
    self.ampWindow.show()


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