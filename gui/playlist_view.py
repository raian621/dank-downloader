from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QScrollArea, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from database import make_session, Playlist

from .media_layout import MediaTable

class PlaylistView(QWidget):
  def __init__(self, parent=None, title=None, goBack=None):
    super().__init__(parent)
    vlayout = QVBoxLayout(self)
    hlayout = QHBoxLayout()
    goBackButton = QPushButton('Go Back')
    goBackButton.clicked.connect(goBack)
    hlayout.addWidget(goBackButton)
    hlayout.addWidget(QLabel(title))
    description = None
    vlayout.addLayout(hlayout)
    with make_session() as session:
      playlist = session.query(Playlist).where(Playlist.name==title).first()
      if playlist:
        description = playlist.description
        self.playlistID = playlist.id
    if description:
      vlayout.addWidget(QLabel(description))
    self.playlistMediaTable = MediaTable(self.playlistID)
    # self.playlistMediaTable.populateTable(self.playlistID)
    vlayout.addWidget(self.playlistMediaTable)
    vlayout.setAlignment(Qt.AlignTop)
