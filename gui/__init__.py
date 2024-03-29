import sys
from PySide6.QtWidgets import QApplication

from .main_window import MainWindow

def show_main_window():
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  # sys.excepthook = window.excepthook
  sys.exit(app.exec_())

if __name__ == '__main__':
  show_main_window()