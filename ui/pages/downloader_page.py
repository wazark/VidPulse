from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QProgressBar,
    QFileDialog, QComboBox, QLabel, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from ui.download_worker import DownloadWorker
from core.downloader import Downloader

import requests
from io import BytesIO


class DownloaderPage(QWidget):
    def __init__(self):
        super().__init__()

        self.mode = "video"
        self.folder_path = None
        self.worker = None

        main_layout = QVBoxLayout()

        # URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Cole o link do vídeo do YouTube")

        # BOTÃO PREVIEW
        self.preview_btn = QPushButton("🔍 Validar vídeo")
        self.preview_btn.clicked.connect(self.load_preview)

        # INFO DO VÍDEO
        self.video_info_label = QLabel("")
        self.video_info_label.setStyleSheet("color: gray;")

        # THUMBNAIL
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedHeight(180)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)

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

        # BOTÃO DOWNLOAD
        self.download_btn = QPushButton("⬇️ Iniciar Download")
        self.download_btn.clicked.connect(self.start_download)

        # BUILD UI
        main_layout.addWidget(self.url_input)
        main_layout.addWidget(self.preview_btn)
        main_layout.addWidget(self.video_info_label)
        main_layout.addWidget(self.thumbnail_label)  # 🔥 IMPORTANTE
        main_layout.addLayout(format_layout)
        main_layout.addLayout(quality_layout)
        main_layout.addLayout(path_layout)
        main_layout.addWidget(self.progress)
        main_layout.addWidget(self.download_btn)

        self.setLayout(main_layout)

        self.update_button_styles()

    # -----------------------------
    # PREVIEW
    # -----------------------------
    def load_preview(self):
        url = self.url_input.text().strip()

        if not url:
            QMessageBox.warning(self, "Aviso", "Insira um link válido.")
            return

        try:
            info = Downloader.get_video_info(url)

            duration = info["duration"]
            minutes = duration // 60 if duration else 0

            self.video_info_label.setText(
                f"🎬 {info['title']}\n"
                f"👤 {info['uploader']}\n"
                f"⏱ {minutes} min"
            )

            # 🔥 CARREGAR THUMBNAIL
            thumbnail_url = info.get("thumbnail")

            if thumbnail_url:
                response = requests.get(thumbnail_url, timeout=5)
                image = QPixmap()
                image.loadFromData(response.content)

                self.thumbnail_label.setPixmap(
                    image.scaled(320, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            else:
                self.thumbnail_label.clear()

        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    # -----------------------------
    # CONTROLES DE MODO
    # -----------------------------
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

    # -----------------------------
    # PASTA
    # -----------------------------
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Escolher pasta")
        if folder:
            self.folder_path = folder

    # -----------------------------
    # DOWNLOAD
    # -----------------------------
    def start_download(self):
        url = self.url_input.text().strip()

        if not url:
            QMessageBox.warning(self, "Aviso", "Insira um link válido.")
            return

        self.download_btn.setEnabled(False)
        self.progress.setValue(0)

        self.worker = DownloadWorker(url, self.mode)

        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_download_finished)
        self.worker.error.connect(self.on_download_error)

        self.worker.start()

    # -----------------------------
    # SUCESSO
    # -----------------------------
    def on_download_finished(self, message):
        QMessageBox.information(self, "Download concluído", message)
        self.reset_ui()

    # -----------------------------
    # ERRO
    # -----------------------------
    def on_download_error(self, error_message):
        QMessageBox.critical(self, "Erro no download", error_message)
        self.reset_ui()

    # -----------------------------
    # RESET UI
    # -----------------------------
    def reset_ui(self):
        self.download_btn.setEnabled(True)
        self.progress.setValue(0)