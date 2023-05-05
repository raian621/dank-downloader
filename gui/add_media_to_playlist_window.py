from PySide6.QtWidgets import QWidget, QScrollArea, QGridLayout, QLabel, QVBoxLayout, QCheckBox, QPushButton
from database import make_session, Playlist, Media, add_media_to_playlist

class PlaylistSelectorTable(QScrollArea):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.checkboxes = []
    self.playlistIDs = []
    self.populateTable()
  
  def populateTable(self):
    widget = QWidget()
    layout = QGridLayout(widget)
    heading = ['TITLE', 'LENGTH', 'COUNT']
    for i in range(len(heading)):
      layout.addWidget(QLabel(heading[i]), 0, i + 1)
    with make_session() as session:
      playlists = session.query(Playlist).all()
      if playlists == None:
        playlists = []
      for i in range(len(playlists)):
        checkbox = QCheckBox()
        self.playlistIDs.append(playlists[i].id)
        self.checkboxes.append(checkbox)
        layout.addWidget(checkbox, i + 1, 0)
        layout.addWidget(QLabel(playlists[i].name), i + 1, 1)
        layout.addWidget(QLabel(str(playlists[i].playlength)), i + 1, 2)
        mediaList = playlists[i].media
        layout.addWidget(QLabel(str(len(mediaList) if mediaList else 0)), i + 1, 3)
    self.setWidget(widget)

  def getSelectedPlaylists(self):
    selectedPlaylistIDs = []
    print(self.checkboxes)
    for i in range(len(self.checkboxes)):
      if self.checkboxes[i].isChecked():
        print(i)
        selectedPlaylistIDs.append(self.playlistIDs[i])

class AddMediaToPlaylistWindow(QWidget):
  def __init__(self, mediaID, parent=None):
    super().__init__(parent)
    layout = QVBoxLayout(self)
    self.mediaID = mediaID
    self.playlistSelectorTable = PlaylistSelectorTable() 
    submit = QPushButton('Submit')
    submit.clicked.connect(self.handleSubmit)
    layout.addWidget(self.playlistSelectorTable)
    layout.addWidget(submit)

  def handleSubmit(self):
    self.playlistSelectorTable.getSelectedPlaylists()
    if self.playlistSelectorTable == None or self.playlistSelectorTable.playlistIDs == None:
      return
    selectedPlaylistIDs = self.playlistSelectorTable.playlistIDs
    print(selectedPlaylistIDs)

    for pid in selectedPlaylistIDs:
      add_media_to_playlist(self.mediaID, pid)
    self.close()

