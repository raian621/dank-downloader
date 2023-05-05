import json

class PlaylistDownloader:
  def __init__(self):
    pass

  def load_configuration(self, filepath=None, config=None):
    if filepath == None and config == None:
      return None
    if filepath != None and config == None:
      with open(filepath) as file:
        config = json.load(file)
    if PlaylistDownloader.valid_config(config):
      self.config = config

  def valid_config(config):
    print("Checking config")
    required_fields = [
      'playlistTitle', 'playlistDescription', 'playlistMedia'
    ]
    for field in required_fields:
      if field not in config:
        return False
    media_configs = config['playlistMedia']
    media_required_fields = [
      'mediaTitle',
      'mediaSubtitle',
      'fileExtension',
      'url'
    ]
    for media_config in media_configs:
      if 'videoData' in media_config:
        if 'resolution' not in media_config['videoData'] or 'fps' not in media_config['videoData']:
          return False
      for field in media_required_fields:
        if field not in media_config:
          return False
    return True
  

  def download(self):
    """
    download files based on the loaded configuration
    """
    if self.config == None:
      return None

  