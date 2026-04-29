import yt_dlp
import os
import sys
from core.utils import get_download_path


def get_ffmpeg_path():
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(__file__))

    return os.path.join(base_path, "ffmpeg")


class Downloader:

    # -----------------------------
    # PREVIEW DO VÍDEO (NOVO)
    # -----------------------------
    @staticmethod
    def get_video_info(url):
        ydl_opts = {
            'quiet': True,
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            return {
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "duration": info.get("duration")
            }

    # -----------------------------
    # DOWNLOAD VIDEO
    # -----------------------------
    @staticmethod
    def download_video(url, progress_hook=None):
        path = get_download_path("video")

        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook] if progress_hook else [],
            'ffmpeg_location': get_ffmpeg_path(),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    # -----------------------------
    # DOWNLOAD AUDIO
    # -----------------------------
    @staticmethod
    def download_audio(url, progress_hook=None):
        path = get_download_path("audio")

        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'format': 'bestaudio',
            'progress_hooks': [progress_hook] if progress_hook else [],
            'ffmpeg_location': get_ffmpeg_path(),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])