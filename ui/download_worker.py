from PySide6.QtCore import QThread, Signal
from core.downloader import Downloader


class DownloadWorker(QThread):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, url, mode):
        super().__init__()
        self.url = url
        self.mode = mode  # "video" ou "audio"

    def run(self):
        try:
            def progress_hook(d):
                if d['status'] == 'downloading':
                    percent = d.get('_percent_str', '0%').replace('%', '').strip()
                    try:
                        self.progress.emit(int(float(percent)))
                    except:
                        pass

            if self.mode == "video":
                Downloader.download_video(self.url, progress_hook)
                self.finished.emit("Vídeo descarregado com sucesso!")
            else:
                Downloader.download_audio(self.url, progress_hook)
                self.finished.emit("Áudio descarregado com sucesso!")

        except Exception as e:
            self.error.emit(str(e))