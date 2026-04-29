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
        """Retorna objeto QSettings configurado para o aplicativo."""
        return QSettings(Config.ORG_NAME, Config.APP_NAME)

    # ---------- TEMA ----------
    @staticmethod
    def get_theme():
        """Retorna o tema salvo ('dark' ou 'light'). Padrão 'dark'."""
        settings = Config.get_settings()
        return settings.value("theme", "dark")

    @staticmethod
    def set_theme(theme):
        """Salva o tema escolhido."""
        settings = Config.get_settings()
        settings.setValue("theme", theme)

    # ---------- IDIOMA ----------
    @staticmethod
    def get_language():
        """Retorna o idioma salvo (código ou nome). Padrão 'Português'."""
        settings = Config.get_settings()
        return settings.value("language", "Português")

    @staticmethod
    def set_language(lang):
        """Salva o idioma escolhido."""
        settings = Config.get_settings()
        settings.setValue("language", lang)

    # ---------- PASTAS PADRÃO ----------
    @staticmethod
    def get_default_video_folder():
        """Retorna a pasta padrão para vídeos."""
        settings = Config.get_settings()
        default = os.path.join(os.path.expanduser("~"), "Videos")
        return settings.value("default_video_folder", default)

    @staticmethod
    def set_default_video_folder(path):
        """Salva a pasta padrão para vídeos."""
        settings = Config.get_settings()
        settings.setValue("default_video_folder", path)

    @staticmethod
    def get_default_audio_folder():
        """Retorna a pasta padrão para áudio."""
        settings = Config.get_settings()
        default = os.path.join(os.path.expanduser("~"), "Music")
        return settings.value("default_audio_folder", default)

    @staticmethod
    def set_default_audio_folder(path):
        """Salva a pasta padrão para áudio."""
        settings = Config.get_settings()
        settings.setValue("default_audio_folder", path)