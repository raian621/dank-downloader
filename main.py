#!./venv/bin/python

from gui import show_main_window
from sys import argv
import os
from downloader.util import *

def main():
    if len(argv) == 2 and argv[1] == 'mock':
        os.environ['MOCK_MODE'] = 'true'
        print(is_mock_mode())
        print('==============================')
        print('PROGRAM STARTING IN MOCK MODE,')
        print('MEDIA WILL NOT BE DOWNLOADED')
        print('==============================')
    show_main_window()
        
if __name__ == '__main__':
    main()