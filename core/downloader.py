import yt_dlp
from core.utils import get_download_path

class Downloader:

    @staticmethod
    def download_video(url):
        path = get_download_path("video")

        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    @staticmethod
    def download_audio(url):
        path = get_download_path("audio")

        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])