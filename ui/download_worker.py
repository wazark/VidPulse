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
            msg = str(e)

            # 🔥 TRATAMENTO DE ERROS MAIS AMIGÁVEL
            if "This video is not available" in msg:
                self.error.emit("Este vídeo não está disponível, foi removido ou está restrito.")
            elif "Private video" in msg:
                self.error.emit("Este vídeo é privado e não pode ser descarregado.")
            elif "Sign in to confirm your age" in msg:
                self.error.emit("Este vídeo possui restrição de idade e requer autenticação.")
            elif "HTTP Error 403" in msg:
                self.error.emit("Acesso negado ao vídeo. Pode estar bloqueado na sua região.")
            else:
                self.error.emit(f"Erro ao processar o download:\n{msg}")