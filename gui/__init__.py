# contains the functions for creating the windows and the gui code

# this is not connected to main as of now

# TO DO
# Add functionality to the buttons (somewhat done)
# Make scrolling areas
# Add downloading functionality

import PySimpleGUI as sg
import gui.modals as modal
from downloader import Downloader

def create_video_options_window(videoURL, fileType):
    url = videoURL
    downloader = Downloader()
    downloader.get_streams(url)

    if fileType == 'Video':
        window = modal.media_video_modal()
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == '-options_video_download-':
                format = values['-format-']
                quality = values['-quality-']
                if format == 'no preference':
                    format = None
                print(url, format, quality)
                downloader.download_video(url, format, quality)
                break
        window.close()
    else:
        window = modal.media_audio_modal()
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == '-options_video_download-':
                format = values['-format-']
                if format == 'no preference':
                    format = None
                print(url, format)
                downloader.download_audio(url, format)
                break
        window.close()

# creates the download media window
def create_media_download_window():
    window = modal.media_download_modal()
    while True:
         event, values = window.read()
         if event == sg.WIN_CLOSED:
            break
         elif event == '-url_page_next-':
             url = values['-url-']
             fileType = values['-format-']
             window.close()
             create_video_options_window(url, fileType)
    window.close()

# creates the main window
def create_main_window():

    # this is a placeholder and can be changed inside the window
    sg.theme('DarkBlue1')

    # the main window
    window = modal.main_window_modal()

    # loops indefinitely
    while True:
       event, values = window.read()
       if event == sg.WIN_CLOSED:
            break
       elif event == '-download_media-':
           create_media_download_window()
    
    window.close()