import os

def get_download_path(file_type="video"):
    home = os.path.expanduser("~")

    if file_type == "audio":
        return os.path.join(home, "Music")
    else:
        return os.path.join(home, "Videos")