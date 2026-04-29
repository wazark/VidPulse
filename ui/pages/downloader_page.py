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


class DownloaderPage(QWidget):
    def __init__(self):
        super().__init__()

        self.mode = "video"
        self.folder_path = None
        self.worker = None
        self.current_video_info = None  # Guarda informações do vídeo atual

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
        self.quality_box.addItem("Auto")

        quality_layout.addWidget(self.quality_label)
        quality_layout.addWidget(self.quality_box)

        # PASTA
        path_layout = QHBoxLayout()

        self.path_label = QLabel("Local de salvamento:")
        self.path_btn = QPushButton("📁 Escolher pasta de destino")
        self.path_btn.clicked.connect(self.select_folder)

        self.path_display = QLabel("")  # 🔥 NOVO: mostra a pasta selecionada
        self.path_display.setStyleSheet("color: #00c853; font-size: 9pt;")

        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_btn)
        path_layout.addWidget(self.path_display)

        # PROGRESSO
        self.progress = QProgressBar()

        # BOTÃO DOWNLOAD
        self.download_btn = QPushButton("⬇️ Iniciar Download")
        self.download_btn.clicked.connect(self.start_download)

        # BUILD UI
        main_layout.addWidget(self.url_input)
        main_layout.addWidget(self.preview_btn)
        main_layout.addWidget(self.video_info_label)
        main_layout.addWidget(self.thumbnail_label)
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
            self.current_video_info = info  # Guarda para uso posterior

            duration = info["duration"]
            minutes = duration // 60 if duration else 0
            hours = minutes // 60 if minutes >= 60 else 0

            if hours > 0:
                duration_text = f"{hours}h {minutes % 60}min"
            else:
                duration_text = f"{minutes} min"

            self.video_info_label.setText(
                f"🎬 {info['title']}\n"
                f"👤 {info['uploader']}\n"
                f"⏱ {duration_text}"
            )

            # Thumbnail
            if info.get("thumbnail"):
                response = requests.get(info["thumbnail"], timeout=5)
                image = QPixmap()
                image.loadFromData(response.content)

                self.thumbnail_label.setPixmap(
                    image.scaled(320, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )

            # Qualidades reais
            self.quality_box.clear()
            self.quality_box.addItem("Auto")

            if info.get("qualities"):
                self.quality_box.addItems(info["qualities"])

            QMessageBox.information(self, "Sucesso", f"Vídeo validado com sucesso!\n\nTítulo: {info['title']}")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar informações do vídeo:\n{str(e)}")

    # -----------------------------
    # CONTROLES DE MODO
    # -----------------------------
    def set_mode(self, mode):
        self.mode = mode
        self.update_button_styles()

        # Ajusta label da qualidade baseado no modo
        if mode == "video":
            self.quality_label.setText("Qualidade do vídeo:")
        else:
            self.quality_label.setText("Qualidade do áudio:")
            self.quality_box.setCurrentText("Auto")

    def update_button_styles(self):
        if self.mode == "video":
            self.btn_video.setStyleSheet("background-color: #00c853; color: black; font-weight: bold;")
            self.btn_audio.setStyleSheet("background-color: #1a1d25;")
        else:
            self.btn_audio.setStyleSheet("background-color: #00c853; color: black; font-weight: bold;")
            self.btn_video.setStyleSheet("background-color: #1a1d25;")

    # -----------------------------
    # PASTA
    # -----------------------------
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Escolher pasta de destino")
        if folder:
            self.folder_path = folder
            # 🔥 MOSTRA A PASTA SELECIONADA NA INTERFACE
            self.path_display.setText(f"📁 {folder}")
        else:
            self.folder_path = None
            self.path_display.setText("")

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

        # Captura qualidade
        selected_quality = self.quality_box.currentText()
        if selected_quality == "Auto":
            selected_quality = None

        # 🔥 USA A PASTA SELECIONADA (se houver)
        output_path = self.folder_path if self.folder_path else None

        # Inicializa worker com a pasta personalizada
        self.worker = DownloadWorker(url, self.mode, selected_quality, output_path)

        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_download_finished)
        self.worker.error.connect(self.on_download_error)

        self.worker.start()

    # -----------------------------
    # SUCESSO
    # -----------------------------
    def on_download_finished(self, message):
        QMessageBox.information(self, "✅ Download concluído", message)
        self.reset_ui()

    # -----------------------------
    # ERRO
    # -----------------------------
    def on_download_error(self, error_message):
        QMessageBox.critical(self, "❌ Erro no download", error_message)
        self.reset_ui()

    # -----------------------------
    # RESET UI
    # -----------------------------
    def reset_ui(self):
        self.download_btn.setEnabled(True)
        self.progress.setValue(0)