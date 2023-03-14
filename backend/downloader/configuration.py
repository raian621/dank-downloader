from downloader.supported_files import *
from database.models import *
import json

class ConfigValMissingError(Exception):
    """
    Exception raised when a configuration value is not present in 
    a configuration file or configuration text
    """
    
    def __init__(self, config_value):
        self.message = f"ConfigValMissingError: '{config_value}' configuration value missing."
        super().__init__(self.message)

def check_configuration(
        configuration:dict
):
    playlist_required_fields = [
        'playlistTitle', 
        'playlistDescription',
        'playlistMedia'
    ]

    media_req_fields = [
        'mediaTitle',
        'mediaSubtitle',
        'url',
        'fileExtension',
    ]

    video_req_fields = [
        'videoData'
    ]

    video_data_req_fields = [
        'resolution',
        'fps'
    ]

    for prf in playlist_required_fields:
        if prf not in configuration.keys:
            raise ConfigValMissingError(prf)

    for media_dict in configuration['playlistMedia']:
        for mrf in media_req_fields:
            if mrf not in media_dict.keys:
                raise ConfigValMissingError(prf)
            if media_dict['fileExtension'] not in (supported_file_formats['video'] | supported_file_formats['audio']):
                raise UnsupportedFileExtError(media_dict['fileExtension'])
            if media_dict['fileExtension'] in supported_file_formats['video']:
                for vrf in video_req_fields:
                    if vrf not in media_dict.keys:
                        raise ConfigValMissingError(vrf)
                    for vdrf in video_data_req_fields:
                        if vdrf not in media_dict['videoData'].keys:
                            raise ConfigValMissingError(vdrf)
                        

def load_configuration(
    configuration_file_path:str=None,
    configuration_text:str=None
) -> dict:
    if configuration_file_path == None and configuration_text == None:
        return None
    configuration_dict = None
    if configuration_file_path == None:
        configuration_dict = json.loads(configuration_text)
    else:
        configuration_dict = json.load(configuration_file_path)
    
    return configuration_dict


def gen_playlist_config(playlist:Playlist) -> dict:
    configuration = {
        'playlistTitle': playlist.name,
        'playlistDescription': playlist.description,
        'playlistMedia': []
    }

    configuration['playlistTitle'] = playlist.name
    configuration['playlistDescription'] = playlist.description

    for media in playlist.media:
        media_dict = {
            'url': media.url,
            'extension': media.extension,
            'mediaTitle': media.title,
            'mediaSubtitle': media.subtitle,
        }
        if media.videodata:
            media_dict['videodata'] = {
                'resolution': media.videodata.resolution,
                'fps': media.videodata.fps,
            }

    return configuration
