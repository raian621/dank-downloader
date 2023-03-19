import os
import re

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