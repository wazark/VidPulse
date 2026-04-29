from PySide6.QtCore import QThread, Signal
from core.downloader import Downloader


class DownloadWorker(QThread):
    progress = Signal(int)
    finished = Signal(str, str)  # (mensagem, caminho_ficheiro)
    error = Signal(str)

    def __init__(self, url, mode, quality=None, output_path=None):
        super().__init__()
        self.url = url
        self.mode = mode
        self.quality = quality
        self.output_path = output_path

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
                file_path = Downloader.download_video(
                    self.url,
                    self.quality,
                    progress_hook,
                    self.output_path
                )
                self.finished.emit("✅ Vídeo descarregado com sucesso!", file_path)
            else:
                file_path = Downloader.download_audio(
                    self.url,
                    progress_hook,
                    self.output_path
                )
                self.finished.emit("✅ Áudio descarregado com sucesso!", file_path)

        except Exception as e:
            msg = str(e)

            if "not available" in msg.lower():
                self.error.emit(
                    "❌ Este vídeo não está disponível.\n\n"
                    "Possíveis causas:\n"
                    "• Vídeo privado ou removido\n"
                    "• Restrição geográfica\n"
                    "• Exige login (use cookies)\n\n"
                    "💡 Dica: Tente baixar com cookies (veja a documentação)"
                )
            elif "Private video" in msg:
                self.error.emit("❌ Este vídeo é privado e não pode ser descarregado.")
            elif "age" in msg.lower() or "sign in" in msg.lower():
                self.error.emit(
                    "❌ Este vídeo tem restrição de idade.\n\n"
                    "Para baixar vídeos com restrição:\n"
                    "1. Faça login no YouTube pelo navegador\n"
                    "2. Use uma extensão para extrair cookies\n"
                    "3. Salve como 'cookies.txt' na pasta do app"
                )
            elif "HTTP Error 403" in msg:
                self.error.emit("❌ Acesso negado ao vídeo. Pode estar bloqueado na sua região.")
            else:
                self.error.emit(f"❌ Erro ao processar o download:\n{msg}")