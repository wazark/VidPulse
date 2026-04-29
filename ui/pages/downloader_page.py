from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QProgressBar,
    QFileDialog, QComboBox, QLabel
)
from ui.download_worker import DownloadWorker


class DownloaderPage(QWidget):
    def __init__(self):
        super().__init__()

        self.mode = "video"
        self.folder_path = None

        main_layout = QVBoxLayout()

        # URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Cole o link do vídeo do YouTube")

        # FORMATO
        format_layout = QHBoxLayout()

        self.btn_video = QPushButton("🎬 MP4")
        self.btn_audio = QPushButton("🎵 MP3")

        self.btn_video.clicked.connect(lambda: self.set_mode("video"))
        self.btn_audio.clicked.connect(lambda: self.set_mode("audio"))

        format_layout.addWidget(self.btn_video)
        format_layout.addWidget(self.btn_audio)

        # QUALIDADE
        quality_layout = QHBoxLayout()

        self.quality_label = QLabel("Qualidade:")
        self.quality_box = QComboBox()
        self.quality_box.addItems([
            "Melhor qualidade automática",
            "1080p",
            "720p",
            "480p"
        ])

        quality_layout.addWidget(self.quality_label)
        quality_layout.addWidget(self.quality_box)

        # PASTA
        path_layout = QHBoxLayout()

        self.path_label = QLabel("Local de salvamento:")
        self.path_btn = QPushButton("📁 Escolher pasta de destino")
        self.path_btn.clicked.connect(self.select_folder)

        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_btn)

        # PROGRESSO
        self.progress = QProgressBar()

        # BOTÃO
        self.download_btn = QPushButton("⬇️ Iniciar Download")
        self.download_btn.clicked.connect(self.start_download)

        # BUILD
        main_layout.addWidget(self.url_input)
        main_layout.addLayout(format_layout)
        main_layout.addLayout(quality_layout)
        main_layout.addLayout(path_layout)
        main_layout.addWidget(self.progress)
        main_layout.addWidget(self.download_btn)

        self.setLayout(main_layout)

        self.update_button_styles()

    def set_mode(self, mode):
        self.mode = mode
        self.update_button_styles()

    def update_button_styles(self):
        if self.mode == "video":
            self.btn_video.setStyleSheet("background-color: #00c853; color: black;")
            self.btn_audio.setStyleSheet("")
        else:
            self.btn_audio.setStyleSheet("background-color: #00c853; color: black;")
            self.btn_video.setStyleSheet("")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Escolher pasta")
        if folder:
            self.folder_path = folder

    def start_download(self):
        url = self.url_input.text().strip()

        if not url:
            return

        self.worker = DownloadWorker(url, self.mode)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.start()