# this is not connected to main as of now

# TO DO
# Add functionality to the buttons
# Make scrolling areas
# Add downloading functionality

# IMPORTANT READ BEFORE EDITING
# the keys to the buttons are in the format -example_button- keep this consistant
# all images go into the assets folder access it with ./assets
# limit the use of whitespace to make text not as long in the window layout


import PySimpleGUI as sg

# set images
# IMPORTANT put all images in the assets folder
doge_image = './assets/dankdownloader.ico'
download_image = './assets/download64x64.png'
plus_image = './assets/plus64x64.png'

# this is a placeholder and can be changed inside the window
sg.theme('DarkBlue1')

def create_main_window():
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

window = create_main_window()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    print('You clicked a button')

window.close()