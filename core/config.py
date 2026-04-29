"""
Módulo de configurações persistentes do VidPulse.
Usa QSettings para salvar preferências entre execuções.
"""
from PySide6.QtCore import QSettings
import os


class Config:
    ORG_NAME = "VidPulse"
    APP_NAME = "VidPulse"

    @staticmethod
    def get_settings():
        return QSettings(Config.ORG_NAME, Config.APP_NAME)

    # ---------- TEMA ----------
    @staticmethod
    def get_theme():
        settings = Config.get_settings()
        return settings.value("theme", "dark")

    @staticmethod
    def set_theme(theme):
        settings = Config.get_settings()
        settings.setValue("theme", theme)

    # ---------- IDIOMA ----------
    @staticmethod
    def get_language():
        settings = Config.get_settings()
        return settings.value("language", "Português")

    @staticmethod
    def set_language(lang):
        settings = Config.get_settings()
        settings.setValue("language", lang)

    # ---------- PASTAS PADRÃO ----------
    @staticmethod
    def get_default_video_folder():
        settings = Config.get_settings()
        default = os.path.join(os.path.expanduser("~"), "Videos")
        return settings.value("default_video_folder", default)

    @staticmethod
    def set_default_video_folder(path):
        settings = Config.get_settings()
        settings.setValue("default_video_folder", path)

    @staticmethod
    def get_default_audio_folder():
        settings = Config.get_settings()
        default = os.path.join(os.path.expanduser("~"), "Music")
        return settings.value("default_audio_folder", default)

    @staticmethod
    def set_default_audio_folder(path):
        settings = Config.get_settings()
        settings.setValue("default_audio_folder", path)

    # ---------- QUALIDADE PADRÃO ----------
    @staticmethod
    def get_default_quality():
        settings = Config.get_settings()
        return settings.value("default_quality", "Auto")

    @staticmethod
    def set_default_quality(quality):
        settings = Config.get_settings()
        settings.setValue("default_quality", quality)

    # ---------- MODO PADRÃO (MP4 ou MP3) ----------
    @staticmethod
    def get_default_format():
        """Retorna 'video' ou 'audio' – modo predefinido (botão MP4/MP3)."""
        settings = Config.get_settings()
        return settings.value("default_format", "video")

    @staticmethod
    def set_default_format(fmt):
        settings = Config.get_settings()
        settings.setValue("default_format", fmt)

    # ---------- FORMATO DE VÍDEO (mp4, webm, mkv) ----------
    @staticmethod
    def get_default_video_format():
        settings = Config.get_settings()
        return settings.value("default_video_format", "mp4")

    @staticmethod
    def set_default_video_format(fmt):
        settings = Config.get_settings()
        settings.setValue("default_video_format", fmt)

    # ---------- FORMATO DE ÁUDIO (mp3, aac, ogg, m4a) ----------
    @staticmethod
    def get_default_audio_format():
        settings = Config.get_settings()
        return settings.value("default_audio_format", "mp3")

    @staticmethod
    def set_default_audio_format(fmt):
        settings = Config.get_settings()
        settings.setValue("default_audio_format", fmt)

    # ---------- DOWNLOADS SIMULTÂNEOS (reservado) ----------
    @staticmethod
    def get_max_concurrent_downloads():
        settings = Config.get_settings()
        return int(settings.value("max_concurrent_downloads", 1))

    @staticmethod
    def set_max_concurrent_downloads(value):
        settings = Config.get_settings()
        settings.setValue("max_concurrent_downloads", value)

    # ---------- VERIFICAR ATUALIZAÇÕES (reservado) ----------
    @staticmethod
    def get_check_updates():
        settings = Config.get_settings()
        return settings.value("check_updates", True, type=bool)

    @staticmethod
    def set_check_updates(enabled):
        settings = Config.get_settings()
        settings.setValue("check_updates", enabled)