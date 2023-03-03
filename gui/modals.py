# contains the modals used for the creation of each window

import PySimpleGUI as sg

# set images
# IMPORTANT put all images in the assets folder
doge_image = './assets/dankdownloader.ico'
download_image = './assets/download64x64.png'
plus_image = './assets/plus64x64.png'

# IMPORTANT READ BEFORE EDITING
# the keys to the buttons are in the format -example_button- keep this consistant
# all images go into the assets folder access it with ./assets
# limit the use of whitespace to make text not as long in the window layout

def main_window_modal():
    # this is what appears inside the window that is created

                # playlist area
    layout = [  [sg.Text('Playlists', font='Roboto 20', text_color='#A7E5FF'),
                 sg.Button(key='-download_playlists-', button_color=(sg.theme_background_color(), sg.theme_background_color()), image_filename=download_image, image_size=(30, 25), image_subsample=2, border_width=0),
                 sg.Button(key='-add_playlists-', button_color=(sg.theme_background_color(), sg.theme_background_color()), image_filename=plus_image, image_size=(30, 30), image_subsample=2, border_width=0)],
                # media area
                [sg.Text('Media    ', font='Roboto 20', text_color='#A7E5FF'),
                 sg.Button(key='-download_media-', button_color=(sg.theme_background_color(), sg.theme_background_color()), image_filename=download_image, image_size=(30, 25), image_subsample=2, border_width=0),
                 sg.Button(key='-add_media-', button_color=(sg.theme_background_color(), sg.theme_background_color()), image_filename=plus_image, image_size=(30, 30), image_subsample=2, border_width=0)]  ]

    window = sg.Window('Dank Downloader', layout, icon=doge_image, size=(900,750))
    return window