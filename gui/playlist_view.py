from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class PlaylistView(QWidget):
  def __init__(self, parent=None, title=None, goBack=None):
    super().__init__(parent)
    vlayout = QVBoxLayout(self)
    hlayout = QHBoxLayout()
    print(title)
    goBackButton = QPushButton('Go Back')
    goBackButton.clicked.connect(goBack)
    hlayout.addWidget(goBackButton)
    hlayout.addWidget(QLabel(title))
    vlayout.addLayout(hlayout)
    vlayout.setAlignment(Qt.AlignTop)

    