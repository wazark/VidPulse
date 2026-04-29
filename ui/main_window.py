from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from core.downloader import Downloader


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Orbytek MediaGrabber")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Cole o link do YouTube:")
        layout.addWidget(self.label)

        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        self.btn_video = QPushButton("Baixar MP4")
        self.btn_video.clicked.connect(self.download_video)
        layout.addWidget(self.btn_video)

        self.btn_audio = QPushButton("Baixar MP3")
        self.btn_audio.clicked.connect(self.download_audio)
        layout.addWidget(self.btn_audio)

        self.setLayout(layout)

    def download_video(self):
        url = self.url_input.text().strip()

        if not url:
            self.show_error("Insere um link válido.")
            return

        try:
            Downloader.download_video(url)
            self.show_success("Download do vídeo concluído!")
        except Exception as e:
            self.show_error(str(e))

    def download_audio(self):
        url = self.url_input.text().strip()

        if not url:
            self.show_error("Insere um link válido.")
            return

        try:
            Downloader.download_audio(url)
            self.show_success("Download do áudio concluído!")
        except Exception as e:
            self.show_error(str(e))

    def show_error(self, message):
        QMessageBox.critical(self, "Erro", message)

    def show_success(self, message):
        QMessageBox.information(self, "Sucesso", message)