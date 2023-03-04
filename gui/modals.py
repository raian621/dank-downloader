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

def media_download_modal():

    layout = [  [sg.Text('Copy and Paste the URL to Download', font='Roboto 12', text_color='#A7E5FF')],
                [sg.InputText(key='-url-'), sg.Combo(['Audio', 'Video'], default_value='Video', key='-format-')],
                [sg.Text('Import Config Settings (Optional)', font='Roboto 12', text_color='#A7E5FF')],
                [sg.Input(), sg.FileBrowse(button_color=('#A7E5FF', sg.theme_background_color()))],
                [sg.Button('Next', key='-url_page_next-', button_color=('#A7E5FF', sg.theme_background_color()))]  ]

    window = sg.Window('Download Media', layout, icon=doge_image, size=(420,160))
    return window

def media_video_modal():

    layout = [  [sg.Text('Select Format', font='Roboto 12', text_color='#A7E5FF')],
                [sg.Combo(['mp4', 'webm', 'no preference'], default_value='mp4', key='-format-')],
                [sg.Text('Select Quality', font='Roboto 12', text_color='#A7E5FF')], 
                [sg.Combo(['1080p', '720p', '480p', '360p', '240p', '144p'], default_value='1080p', key='-quality-')],
                [sg.Button('Download', key='-options_video_download-', button_color=('#A7E5FF', sg.theme_background_color()))]   ]

    window = sg.Window('Download Media', layout, icon=doge_image, size=(420,160))
    return window

def media_audio_modal():

    layout = [  [sg.Text('Select Format', font='Roboto 12', text_color='#A7E5FF')],
                [sg.Combo(['mp3', 'wav', 'no preference'], default_value='mp3', key='-format-')],
                [sg.Button('Download', key='-options_video_download-', button_color=('#A7E5FF', sg.theme_background_color()))]   ]

    window = sg.Window('Download Media', layout, icon=doge_image, size=(420,120))
    return window