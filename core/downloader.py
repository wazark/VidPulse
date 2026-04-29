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

    @staticmethod
    def get_cookie_file():
        """Retorna o caminho do arquivo de cookies se existir."""
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(__file__))

        cookie_path = os.path.join(base_path, "cookies.txt")
        user_cookie_path = os.path.join(os.path.expanduser("~"), ".vidpulse", "cookies.txt")

        if os.path.exists(cookie_path):
            return cookie_path
        elif os.path.exists(user_cookie_path):
            return user_cookie_path
        else:
            return None

    @staticmethod
    def get_extractor_args():
        """Define os clients do YouTube a serem tentados (fallback automático)."""
        return {
            'youtube': {
                'player_client': ['default', 'web_safari', 'android', 'ios'],
                'skip': ['webpage']
            }
        }

    # -----------------------------
    # PREVIEW + FORMATOS + TAMANHO ESTIMADO
    # -----------------------------
    @staticmethod
    def get_video_info(url):
        """Retorna informações do vídeo, incluindo tamanho estimado em MB."""
        cookie_file = Downloader.get_cookie_file()

        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'ffmpeg_location': get_ffmpeg_path(),
            'ignoreerrors': True,
            'extract_flat': False,
            'extractor_args': Downloader.get_extractor_args(),
        }

        if cookie_file:
            ydl_opts['cookiefile'] = cookie_file

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                if info is None:
                    raise Exception("Vídeo não disponível ou restrito")

                formats = info.get("formats", [])

                qualities = set()
                format_map = {}
                best_filesize = None

                for f in formats:
                    # Captura tamanho do melhor formato (vídeo+áudio combinados)
                    if f.get("filesize") and (best_filesize is None or f["filesize"] > best_filesize):
                        best_filesize = f["filesize"]

                    if f.get("height"):
                        quality = f"{f['height']}p"
                        qualities.add(quality)

                        if quality not in format_map or f.get("tbr", 0) > format_map[quality]["tbr"]:
                            format_map[quality] = {
                                "format_id": f["format_id"],
                                "tbr": f.get("tbr", 0)
                            }

                qualities = sorted(qualities, key=lambda x: int(x.replace("p", "")), reverse=True)

                # Se não encontrou filesize, tenta estimar via tamanho dos requests
                if best_filesize is None and info.get("filesize"):
                    best_filesize = info["filesize"]

                # Converte bytes para MB (arredondado)
                size_mb = round(best_filesize / (1024 * 1024), 1) if best_filesize else None

                return {
                    "title": info.get("title", "Título desconhecido"),
                    "uploader": info.get("uploader", "Autor desconhecido"),
                    "duration": info.get("duration", 0),
                    "thumbnail": info.get("thumbnail"),
                    "qualities": qualities,
                    "format_map": format_map,
                    "filesize_mb": size_mb,          # 🔥 NOVO: tamanho estimado
                }
        except Exception as e:
            error_msg = str(e)
            if "This video is not available" in error_msg:
                raise Exception("Este vídeo não está disponível (pode ser restrito por região ou exigir login). Tente usar um arquivo de cookies.")
            elif "Private video" in error_msg:
                raise Exception("Este vídeo é privado e não pode ser acessado.")
            elif "age" in error_msg.lower():
                raise Exception("Este vídeo tem restrição de idade e requer autenticação.")
            else:
                raise Exception(f"Erro ao obter informações: {error_msg}")

    # -----------------------------
    # DOWNLOAD VIDEO (COM MULTI-CLIENT + FALLBACK)
    # -----------------------------
    @staticmethod
    def download_video(url, quality=None, progress_hook=None, output_path=None):
        if output_path is None:
            path = get_download_path("video")
        else:
            path = output_path

        os.makedirs(path, exist_ok=True)
        cookie_file = Downloader.get_cookie_file()

        if quality:
            height = int(quality.replace("p", ""))
            format_str = f"bestvideo[ext=mp4][height<={height}]+bestaudio[ext=m4a]/bestvideo[ext=mp4][height<={height}]+bestaudio/best[ext=mp4]"
        else:
            format_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"

        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'format': format_str,
            'merge_output_format': 'mp4',
            'postprocessors': [],
            'progress_hooks': [progress_hook] if progress_hook else [],
            'ffmpeg_location': get_ffmpeg_path(),
            'prefer_ffmpeg': True,
            'fixup': 'detect_or_warn',
            'ignoreerrors': True,
            'extract_flat': False,
            'extractor_args': Downloader.get_extractor_args(),
        }

        if cookie_file:
            ydl_opts['cookiefile'] = cookie_file

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            error_msg = str(e)
            if "not available" in error_msg.lower() or "requested format" in error_msg.lower():
                if progress_hook:
                    progress_hook({'status': 'downloading', '_percent_str': '0%'})

                fallback_opts = {
                    'outtmpl': f'{path}/%(title)s.%(ext)s',
                    'format': 'best[ext=mp4]/best',
                    'merge_output_format': 'mp4',
                    'postprocessors': [],
                    'progress_hooks': [progress_hook] if progress_hook else [],
                    'ffmpeg_location': get_ffmpeg_path(),
                    'ignoreerrors': True,
                    'extractor_args': Downloader.get_extractor_args(),
                }
                if cookie_file:
                    fallback_opts['cookiefile'] = cookie_file

                with yt_dlp.YoutubeDL(fallback_opts) as ydl:
                    ydl.download([url])
            else:
                raise e

    # -----------------------------
    # DOWNLOAD AUDIO
    # -----------------------------
    @staticmethod
    def download_audio(url, progress_hook=None, output_path=None):
        if output_path is None:
            path = get_download_path("audio")
        else:
            path = output_path

        os.makedirs(path, exist_ok=True)
        cookie_file = Downloader.get_cookie_file()

        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'progress_hooks': [progress_hook] if progress_hook else [],
            'ffmpeg_location': get_ffmpeg_path(),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ignoreerrors': True,
            'extractor_args': Downloader.get_extractor_args(),
        }

        if cookie_file:
            ydl_opts['cookiefile'] = cookie_file

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])