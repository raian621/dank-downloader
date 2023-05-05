from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QGridLayout, QMenu
from .playlist_windows import *
from database import make_session, Playlist, delete_playlist

class PlaylistTable(QScrollArea):
  def __init__(self, parent=None, showPlaylistView=None):
    super().__init__(parent)
    self.rows = None
    self.contextMenus = []
    self.playlistIDs = []
    self.populateTable()
    self.showPlaylistView = showPlaylistView

  def populateTable(self):
    widget = QWidget()
    widget.setLayout(QGridLayout())
    self.heading = ['TITLE', 'LENGTH', 'COUNT', 'OPTIONS']
    
    if self.rows == None:
      self.rows = []
      self.getPlaylistsFromDB()

    for i in range(len(self.heading)):
      widget.layout().addWidget(QLabel(self.heading[i]), 0, i + 1)

    for i in range(len(self.rows)):
      button = QPushButton('Open')
      name = self.rows[i][0]
      button.clicked.connect(lambda _='', playlistName=name: self.showPlaylistView(playlistName))
      print("A", self.rows[i][0])
      widget.layout().addWidget(button, i + 1, 0)
      n_variables = len(self.rows[i])
      for j in range(n_variables):
        widget.layout().addWidget(QLabel(str(self.rows[i][j])), i + 1, j + 1)
      contextMenu = QMenu()
      self.contextMenus.append(contextMenu)
      if i == len(self.playlistIDs):
        playlistID = 0
        with make_session() as session:
          playlist = session.query(Playlist).where(Playlist.name==self.rows[i][0]).first()
          playlistID = playlist.id
        self.playlistIDs.append(playlistID)
      contextMenu.addAction("Delete", lambda playlistID=self.playlistIDs[i]: self.deletePlaylist(playlistID))
      button = QPushButton('Options')
      button.setMenu(contextMenu)
      widget.layout().addWidget(button, i + 1, n_variables + 1)
    print("A", self.rows)
    self.setWidget(widget)

  def getPlaylistsFromDB(self):
    with make_session() as session:
      playlistList = session.query(Playlist).all()
      for playlist in playlistList:
        row = [
          f'{playlist.name}', # title
          # f'{playlist.description[:10]}',
          f"{playlist.playlength}",
          len(playlist.media) if playlist.media else 0,
        ]
        self.rows.append(row)
        self.playlistIDs.append(playlist.id)

  def deletePlaylist(self, playlistID):
    self.rows = None
    delete_playlist(playlistID)
    self.populateTable()
  
class PlaylistLayout(QVBoxLayout):
  def __init__(self, parent=None, showPlaylistView=None):
    super().__init__(parent)

    downloadButton = QPushButton("Download")
    downloadButton.clicked.connect(self.showDownloadWindow)
    addButton = QPushButton("Add")
    addButton.clicked.connect(self.showAddWindow)
    label = QLabel("PLAYLISTS")
    self.playlistTable = PlaylistTable(showPlaylistView=showPlaylistView)
    barLayout = QHBoxLayout()
    barLayout.addWidget(label)
    barLayout.addWidget(downloadButton)
    barLayout.addWidget(addButton)
    layout = QVBoxLayout()
    layout.addLayout(barLayout)
    layout.addWidget(self.playlistTable)
    self.addLayout(layout)

  def showDownloadWindow(self):
    self.dlWindow = PlaylistDownloadWindow()
    self.dlWindow.repopulateTable = self.playlistTable.populateTable
    self.dlWindow.rows = self.playlistTable.rows
    self.dlWindow.show()

  def showAddWindow(self):
    self.dlWindow = PlaylistCreationWindow()
    self.dlWindow.repopulateTable = self.playlistTable.populateTable
    self.dlWindow.rows = self.playlistTable.rows
    self.dlWindow.show()