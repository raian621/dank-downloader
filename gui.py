# this is test code not intended for the release
# this is not connected to main as of now

# TO DO
# Make custom theme
# Make homepage
# Add downloading

import PySimpleGUI as sg

# set button images
download_icon = './assets/download.png'
plus_icon = './assets/download.png'

sg.theme('DarkBlue1')

def create_window():
    # this is what appears inside the window that is created
    layout = [  [sg.Text('Playlists', font='Roboto 20', text_color='#A7E5FF')],
                [sg.Text('Media', font='Roboto 20', text_color='#A7E5FF')]  ]

    window = sg.Window('Dank Downloader', layout, icon='./assets/dankdownloader.ico', size=(900,750))
    return window

window = create_window()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    print('You entered', values[0])

window.close()