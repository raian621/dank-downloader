import os
import re
import hashlib

from database import make_session, get_user
from database.models import *

# initialize the default download directory
DOWNLOAD_DIRECTORY = os.path.join(os.path.expanduser('~'), "dank-downloader")
print(DOWNLOAD_DIRECTORY)
if os.path.exists(DOWNLOAD_DIRECTORY) == False:
    os.makedirs(DOWNLOAD_DIRECTORY)


def on_progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    percent_complete = (total_size - bytes_remaining) / total_size
    progress_line_end = "\r" if percent_complete < 1 else "\n"
    print("Download {:.2f}% complete".format(percent_complete * 100), end=progress_line_end)

def download_stream(stream, file_path):
    """
    Downloads a stream to the given file path.
    Used as a target for threads.
    ---------------------------------------------------------------
    
    params:
        stream: the stream to download
        file_path: the path to save the media at.
    """
    try:
        stream.download(filename=file_path)
    except Exception as e:
        print(e)

def resolution_to_int(res):
    num = re.findall('([0-9]+)', res)[0]
    return int(num)


def create_media_hash(attr) -> str:
    """
    creates a sha256 hash for an array of data
    """
    
    hasher = hashlib.sha256()
    hasher.update(repr(attr).encode())
    return hasher.hexdigest() 


def add_media_to_db(media_info:dict, is_video:bool):
    stuff_to_hash = [
        media_info["playlength"],
        media_info["extension"],
        media_info["url"],
        media_info["filepath"],
        media_info["title"],
        media_info["subtitle"]
    ]
    if is_video:
        stuff_to_hash.append(media_info["resolution"])
        stuff_to_hash.append(media_info["fps"])
    else:
        stuff_to_hash.append(media_info["bitrate"])
    media_hash = create_media_hash(stuff_to_hash)

    with make_session() as session:
        if session.query(Media).where(Media.media_hash==media_hash).first():
            print("MEDIA EXISTS")
            return

        user = get_user(session)
        media = Media(
            media_info["playlength"],
            media_info["extension"],
            media_info["url"],
            media_info["filepath"],
            media_info["title"],
            media_info["subtitle"],
            user
        )
        
        if is_video:
            media.videodata = VideoData(media_info["resolution"], media_info["fps"], media)
        media.media_hash = media_hash

        user.media.append(media)
        session.add(user)
        session.commit()
      