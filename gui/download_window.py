from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QComboBox, QLineEdit, QFormLayout, QMainWindow
from downloader import MediaDownloadInfo, MediaManager
from .progress_window import ProgressWindow
from downloader.util import MOCK_MODE

class URLFormWindow(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.urlLine = QLineEdit()
    self.fileType = QComboBox()
    self.fileType.addItems(['Video', 'Audio'])

    self.mediaInfo = MediaDownloadInfo()

    submit = QPushButton("Submit")
    submit.clicked.connect(self.submit)

    flo = QFormLayout()
    flo.addRow("Youtube URL", self.urlLine)
    flo.addRow("File Type", self.fileType)
    flo.addRow(submit)
    self.setLayout(flo)

  def submit(self):
    self.url = self.urlLine.text()
    self.file_type = self.fileType.currentText()
    self.showVideoSettings() if self.file_type == 'Video' else self.showAudioSettings()


class VideoFormWindow(QWidget):
  def __init__(self, extensions, resolutions, parent=None):
    super().__init__(parent)
    self.extension = QComboBox()
    self.extension.addItems(extensions)
    self.resolution = QComboBox()
    self.resolution.addItems(resolutions)

    submit = QPushButton("Submit")
    submit.clicked.connect(self.submit)

    flo = QFormLayout()
    flo.addRow("Extension", self.extension)
    flo.addRow("Resolution", self.resolution)
    flo.addRow(submit)
    self.setLayout(flo)

  def submit(self):
    self.file_extension = self.extension.currentText()
    self.video_resolution = self.resolution.currentText()
    self.submitForm()
    

class AudioFormWindow(QWidget):
  def __init__(self, extensions, parent=None):
    super().__init__(parent)
    self.extension = QComboBox()
    self.extension.addItems(extensions)

    submit = QPushButton("Submit")
    submit.clicked.connect(self.submit)

    flo = QFormLayout()
    flo.addRow("Extension", self.extension)
    flo.addRow(submit)
    self.setLayout(flo)

  def submit(self):
    self.file_extension = self.extension.currentText()
    self.submitForm()


class MediaDownloadWindow(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.showURLForm()

  def showURLForm(self):
    self.urlForm = URLFormWindow()
    self.setWindowTitle("Enter URL and Media Type")
    self.setCentralWidget(self.urlForm)
    self.urlForm.showVideoSettings = self.showVideoSettings
    self.urlForm.showAudioSettings = self.showAudioSettings


  def showVideoSettings(self):
    self.downloader = MediaManager(self.urlForm.url)
    if MOCK_MODE == False:
      self.downloader.get_streams()
    
    self.extensions = self.downloader.get_formats()
    self.resolutions = self.downloader.get_resolutions()
    self.videoSettings = VideoFormWindow(self.extensions, self.resolutions)
    self.setWindowTitle("Select Video Settings")
    self.setCentralWidget(self.videoSettings)
    self.videoSettings.submitForm = self.submit


  def showAudioSettings(self):
    self.downloader = MediaManager(self.urlForm.url)
    if MOCK_MODE == False:
      self.downloader.get_streams()

    self.extensions = self.downloader.get_formats(is_audio=True)
    self.audioSettings = AudioFormWindow(self.extensions)
    self.setWindowTitle("Select Audio Settings")
    self.setCentralWidget(self.audioSettings)
    self.audioSettings.submitForm = self.submit

  def showProgressWindow(self):
    self.progressWindow = ProgressWindow()
    self.progressWindow.show()

  def submit(self):
    media_info = None
    self.showProgressWindow()
    if self.urlForm.file_type == "Video":
      media_info = self.downloader.download_video(
        file_extension=self.videoSettings.file_extension,
        resolution=self.videoSettings.video_resolution
      )
    else:
      media_info = self.downloader.download_audio(
        file_extension=self.audioSettings.file_extension
      )

    self.rows.append([
      [f'{media_info["title"]}', f'{media_info["subtitle"]}'],
      media_info["extension"],
      f'{media_info["playlength"]}',
      media_info["filepath"],
    ])
    
    self.progressWindow.close()
    self.repopulateTable()
    self.close()
