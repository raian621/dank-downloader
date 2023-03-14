# Dank Downloader

## Team
Dank Memers
- Ryan Bell
- Joshua Turcotte
- Cade Howard

### To install requirements:

```sh
pip install -r requirements.txt
```

### To launch the program:

```sh
python main.py
```

## Example Playlist Configuration File

```json
{
  "playlistTitle": "Title",
  "playlistDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
  "playlistMedia": [
    {
      "mediaTitle": "Never Gonna Give You Up [Music Video]",
      "mediaSubtitle": "Subtitle",
      "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "fileExtension": "mp4",
      "videoData": {
        "resolution": "720p",
        "fps": 25
      }
    },
    {
      "mediaTitle": "Never Gonna Give You Up [Audio]",
      "mediaSubtitle": "Subtitle",
      "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "fileExtension": "mp3"
    }
  ]
}
```