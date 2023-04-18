from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QUrl

class MediaPlayer(QWidget):
    def __init__(self, media_list, parent=None):
        super(MediaPlayer, self).__init__(parent)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.setGeometry(100, 100, 640, 480)

        videoWidget = QVideoWidget()
        self.layout = QVBoxLayout(self)
        self.layout.addChildWidget(videoWidget)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.open_file(media_list[0])
        self.media_index = 0
        # self.stateChanged.connect(self.mediaStateChanged)
        
        self.play()
        self.show()
        
    def media_state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            pass
        else:
            pass

    def open_file(self, filepath):
        print(filepath)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filepath)))

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def back(self):
        self.media_index = (self.media_index - 1) % len(self.media_index)
        self.open_file(self.media_list[self.media_index])
        self.play()

    def skip(self):
        self.media_index = (self.media_index + 1) % len(self.media_index)
        self.open_file(self.media_list[self.media_index])
        self.play()
