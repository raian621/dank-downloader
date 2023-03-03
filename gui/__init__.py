# contains the functions for creating the windows and the gui code

# this is not connected to main as of now

# TO DO
# Add functionality to the buttons
# Make scrolling areas
# Add downloading functionality

import PySimpleGUI as sg
import modals as modal

def create_main_window():
    # this is a placeholder and can be changed inside the window
    sg.theme('DarkBlue1')

    window = modal.main_window_modal()

    while True:
       event, values = window.read()
       if event == sg.WIN_CLOSED:
            break
       print('You clicked a button')

    window.close()

create_main_window()