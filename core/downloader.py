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
    # PREVIEW + FORMATOS
    # -----------------------------
    @staticmethod
    def get_video_info(url):
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'ffmpeg_location': get_ffmpeg_path()
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            formats = info.get("formats", [])

            qualities = set()
            format_map = {}  # Mapeia qualidade -> format_id

            for f in formats:
                if f.get("height"):
                    quality = f"{f['height']}p"
                    qualities.add(quality)

                    # Guarda o melhor format_id para cada qualidade
                    if quality not in format_map or f.get("tbr", 0) > format_map[quality]["tbr"]:
                        format_map[quality] = {
                            "format_id": f["format_id"],
                            "tbr": f.get("tbr", 0)
                        }

            qualities = sorted(
                qualities,
                key=lambda x: int(x.replace("p", "")),
                reverse=True
            )

            return {
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail"),
                "qualities": qualities,
                "format_map": format_map  # Retorna também o mapeamento
            }

    # -----------------------------
    # DOWNLOAD VIDEO (CORRIGIDO - COMPATÍVEL COM WMP)
    # -----------------------------
    @staticmethod
    def download_video(url, quality=None, progress_hook=None, output_path=None):
        # Usa pasta personalizada ou padrão
        if output_path is None:
            path = get_download_path("video")
        else:
            path = output_path

        # Garante que o diretório existe
        os.makedirs(path, exist_ok=True)

        # Estratégia de formatos compatíveis (CORREÇÃO PRINCIPAL)
        if quality:
            # Extrai altura da qualidade (ex: "1080p" -> 1080)
            height = int(quality.replace("p", ""))

            # 🔥 SOLUÇÃO: Força MP4 video + M4A audio (AAC codec)
            # Isso garante compatibilidade com Windows Media Player
            format_str = f"bestvideo[ext=mp4][height<={height}]+bestaudio[ext=m4a]/bestvideo[ext=mp4][height<={height}]+bestaudio/best[ext=mp4]"
        else:
            # Modo automático - prioriza MP4 + M4A
            format_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"

        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',

            # 🔥 FORMATO PRIORITÁRIO (MP4 container + AAC audio)
            'format': format_str,

            # 🔥 Força merge para MP4
            'merge_output_format': 'mp4',

            # 🔥 Post-processadores mínimos (evita conversão desnecessária)
            'postprocessors': [],

            'progress_hooks': [progress_hook] if progress_hook else [],
            'ffmpeg_location': get_ffmpeg_path(),

            # 🔥 Opções para melhor compatibilidade
            'prefer_ffmpeg': True,
            'fixup': 'detect_or_warn',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    # -----------------------------
    # DOWNLOAD AUDIO
    # -----------------------------
    @staticmethod
    def download_audio(url, progress_hook=None, output_path=None):
        # Usa pasta personalizada ou padrão
        if output_path is None:
            path = get_download_path("audio")
        else:
            path = output_path

        # Garante que o diretório existe
        os.makedirs(path, exist_ok=True)

        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'progress_hooks': [progress_hook] if progress_hook else [],
            'ffmpeg_location': get_ffmpeg_path(),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Converte para MP3 (mais compatível)
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])