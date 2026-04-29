import yt_dlp
import os
import sys
from core.utils import get_download_path
from core.config import Config  # 🔥 Importar Config


def get_ffmpeg_path():
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_path, "ffmpeg")


class Downloader:

    @staticmethod
    def get_cookie_file():
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
        return None

    @staticmethod
    def get_extractor_args():
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
                    if f.get("filesize") and (best_filesize is None or f["filesize"] > best_filesize):
                        best_filesize = f["filesize"]
                    if f.get("height"):
                        quality = f"{f['height']}p"
                        qualities.add(quality)
                        if quality not in format_map or f.get("tbr", 0) > format_map[quality]["tbr"]:
                            format_map[quality] = {"format_id": f["format_id"], "tbr": f.get("tbr", 0)}

                qualities = sorted(qualities, key=lambda x: int(x.replace("p", "")), reverse=True)
                if best_filesize is None and info.get("filesize"):
                    best_filesize = info["filesize"]
                size_mb = round(best_filesize / (1024 * 1024), 1) if best_filesize else None

                return {
                    "title": info.get("title", "Título desconhecido"),
                    "uploader": info.get("uploader", "Autor desconhecido"),
                    "duration": info.get("duration", 0),
                    "thumbnail": info.get("thumbnail"),
                    "qualities": qualities,
                    "format_map": format_map,
                    "filesize_mb": size_mb,
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
    # DOWNLOAD VIDEO (com formato configurável)
    # -----------------------------
    @staticmethod
    def download_video(url, quality=None, progress_hook=None, output_path=None):
        if output_path is None:
            path = get_download_path("video")
        else:
            path = output_path

        os.makedirs(path, exist_ok=True)
        cookie_file = Downloader.get_cookie_file()

        # Obtém formato de vídeo escolhido nas configurações
        video_format = Config.get_default_video_format()  # mp4, webm, mkv

        # Configuração base com qualidade
        if quality:
            height = int(quality.replace("p", ""))
            # Prioriza melhor vídeo compatível com o formato desejado e áudio separado
            # Nota: para webm/mkv, o áudio pode estar em opus; tentamos m4a como fallback
            if video_format == 'mp4':
                format_str = f"bestvideo[ext=mp4][height<={height}]+bestaudio[ext=m4a]/bestvideo[ext=mp4][height<={height}]+bestaudio/best[ext=mp4]"
            else:
                # Para webm/mkv, permite vídeo no formato desejado e áudio opus ou m4a
                format_str = f"bestvideo[ext={video_format}][height<={height}]+bestaudio/best[ext={video_format}]"
        else:
            if video_format == 'mp4':
                format_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"
            else:
                format_str = f"bestvideo[ext={video_format}]+bestaudio/best[ext={video_format}]"

        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'format': format_str,
            'merge_output_format': video_format,  # Define o container final
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
                info = ydl.extract_info(url, download=True)
                base_filename = ydl.prepare_filename(info)
                final_path = base_filename if base_filename.endswith(f'.{video_format}') else base_filename + f'.{video_format}'
                if not os.path.exists(final_path):
                    for f in os.listdir(path):
                        if f.endswith(f'.{video_format}') and info['title'] in f:
                            final_path = os.path.join(path, f)
                            break
                return final_path
        except Exception as e:
            error_msg = str(e)
            # Fallback sem formatação específica
            if "not available" in error_msg.lower() or "requested format" in error_msg.lower():
                if progress_hook:
                    progress_hook({'status': 'downloading', '_percent_str': '0%'})

                fallback_opts = {
                    'outtmpl': f'{path}/%(title)s.%(ext)s',
                    'format': 'best[ext=mp4]/best',  # fallback para mp4
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
                    info = ydl.extract_info(url, download=True)
                    base_filename = ydl.prepare_filename(info)
                    final_path = base_filename if base_filename.endswith('.mp4') else base_filename + '.mp4'
                    if not os.path.exists(final_path):
                        for f in os.listdir(path):
                            if f.endswith('.mp4') and info['title'] in f:
                                final_path = os.path.join(path, f)
                                break
                    return final_path
            else:
                raise e

    # -----------------------------
    # DOWNLOAD AUDIO (com formato configurável)
    # -----------------------------
    @staticmethod
    def download_audio(url, progress_hook=None, output_path=None):
        if output_path is None:
            path = get_download_path("audio")
        else:
            path = output_path

        os.makedirs(path, exist_ok=True)
        cookie_file = Downloader.get_cookie_file()

        # Obtém formato de áudio escolhido
        audio_format = Config.get_default_audio_format()  # mp3, aac, ogg, m4a
        # Mapeamento codec para yt-dlp
        codec_map = {
            'mp3': 'mp3',
            'aac': 'aac',
            'ogg': 'vorbis',
            'm4a': 'm4a'
        }
        preferred_codec = codec_map.get(audio_format, 'mp3')
        # yt-dlp suporta 'bestaudio' e depois converte
        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'progress_hooks': [progress_hook] if progress_hook else [],
            'ffmpeg_location': get_ffmpeg_path(),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': preferred_codec,
                'preferredquality': '192',
            }],
            'ignoreerrors': True,
            'extractor_args': Downloader.get_extractor_args(),
        }

        if cookie_file:
            ydl_opts['cookiefile'] = cookie_file

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            base_filename = ydl.prepare_filename(info)
            base_without_ext = os.path.splitext(base_filename)[0]
            final_path = base_without_ext + f'.{audio_format}'
            if not os.path.exists(final_path):
                for f in os.listdir(path):
                    if f.endswith(f'.{audio_format}') and info['title'] in f:
                        final_path = os.path.join(path, f)
                        break
            return final_path