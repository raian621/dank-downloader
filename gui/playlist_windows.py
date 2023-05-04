from PySide6.QtWidgets import QWidget, QPlainTextEdit, QFormLayout, QPushButton, QLineEdit, QFileDialog, QHBoxLayout
from database import create_playlist

class PlaylistCreationWindow(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    flo = QFormLayout()
    
    self.titleInput = QLineEdit()
    flo.addRow('Title:', self.titleInput)
    self.descInput = QPlainTextEdit()
    flo.addRow('Description:', self.descInput)
    submit = QPushButton('Submit')
    submit.clicked.connect(self.handleSubmit)
    flo.addRow(submit)

    self.setLayout(flo)

  def handleSubmit(self):
    title = self.titleInput.text()
    description = self.descInput.toPlainText()
    if title == '' or description == '':
      return
  
    create_playlist(title, description)
    self.rows.append([
      self.titleInput.text(),
      0,
      0,
      'options'
    ])

    print(title, description)
    self.repopulateTable()
    self.close()

class PlaylistDownloadWindow(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    flo = QFormLayout()
    
    self.textInput = QPlainTextEdit()
    flo.addRow('Text Input:', self.textInput)
    self.fileDialogButton = QPushButton('Browse')
    self.fileDialogButton.clicked.connect(self.selectFile)
    self.filepathInput = QLineEdit()
    fil = QHBoxLayout()
    fil.addWidget(self.fileDialogButton)
    fil.addWidget(self.filepathInput)
    flo.addRow('File Input:', fil)
    submit = QPushButton('Submit')
    submit.clicked.connect(self.handleSubmit)
    flo.addRow(submit)

    self.setLayout(flo)

  def selectFile(self):
    filepath = QFileDialog.getOpenFileName(self, "Open File", "", "*.json")[0]
    self.filepathInput.setText(filepath)

  def handleSubmit(self):
    self.close()
  