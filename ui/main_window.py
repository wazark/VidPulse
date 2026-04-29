from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QProgressBar
)
from ui.download_worker import DownloadWorker


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VidPulse")
        self.setFixedSize(400, 250)

        layout = QVBoxLayout()

        self.label = QLabel("Cole o link do YouTube:")
        layout.addWidget(self.label)

        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.btn_video = QPushButton("Baixar MP4")
        self.btn_video.clicked.connect(self.download_video)
        layout.addWidget(self.btn_video)

        self.btn_audio = QPushButton("Baixar MP3")
        self.btn_audio.clicked.connect(self.download_audio)
        layout.addWidget(self.btn_audio)

        self.setLayout(layout)

        self.worker = None

    def start_download(self, mode):
        url = self.url_input.text().strip()

        if not url:
            self.show_error("Insere um link válido.")
            return

        self.btn_video.setEnabled(False)
        self.btn_audio.setEnabled(False)
        self.progress_bar.setValue(0)

        self.worker = DownloadWorker(url, mode)

        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.download_finished)
        self.worker.error.connect(self.download_error)

        self.worker.start()

    def download_video(self):
        self.start_download("video")

    def download_audio(self):
        self.start_download("audio")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def download_finished(self, message):
        self.show_success(message)
        self.reset_ui()

    def download_error(self, message):
        self.show_error(message)
        self.reset_ui()

    def reset_ui(self):
        self.btn_video.setEnabled(True)
        self.btn_audio.setEnabled(True)
        self.progress_bar.setValue(0)

    def show_error(self, message):
        QMessageBox.critical(self, "Erro", message)

    def show_success(self, message):
        QMessageBox.information(self, "Sucesso", message)