# contains the functions for creating the windows and the gui code

# this is not connected to main as of now

# TO DO
# Add functionality to the buttons
# Make scrolling areas
# Add downloading functionality

import PySimpleGUI as sg
import modals as modal

def create_media_options_window(videoURL):
    url = videoURL
    window = modal.media_options_modal()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-options_page_download-':
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
             url = values[0]
             window.close()
             print(url)
             create_media_options_window(url)
             break
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

create_main_window()