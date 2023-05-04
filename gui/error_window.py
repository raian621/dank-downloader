from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QPixmap

class ErrorWindow(QWidget):
  def __init__(self, parent=None, err_val=None, err_type=None):
    super().__init__(parent)
    self.setWindowTitle(err_type)
    layout = QVBoxLayout()
    image = QLabel()
    image.setPixmap(QPixmap('assets/Doge-Crying.jpg'))
    image.setMaximumHeight(300)
    message = QLabel(err_val)
    exitButton = QPushButton('OK')
    exitButton.clicked.connect(lambda: self.close())
    layout.addWidget(image)
    layout.addWidget(message)
    layout.addWidget(exitButton)
    self.setLayout(layout)