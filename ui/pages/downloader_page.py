from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QProgressBar,
    QFileDialog, QComboBox, QLabel, QMessageBox, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from ui.download_worker import DownloadWorker
from core.downloader import Downloader
from core.config import Config  # 🔥 Para carregar pasta padrão

import requests
import os


class DownloaderPage(QWidget):
    def __init__(self):
        super().__init__()

        self.mode = "video"
        self.folder_path = None
        self.worker = None
        self.current_video_info = None

        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Cole o link do vídeo do YouTube")

        # Preview button
        self.preview_btn = QPushButton("🔍 Validar vídeo")
        self.preview_btn.clicked.connect(self.load_preview)

        # Info labels (agora com tamanho)
        self.video_info_label = QLabel("")
        self.video_info_label.setStyleSheet("color: #7A7E8F; font-size: 10pt;")
        self.video_info_label.setWordWrap(True)

        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedHeight(180)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)

        # Format selection
        format_layout = QHBoxLayout()
        self.btn_video = QPushButton("🎬 MP4")
        self.btn_audio = QPushButton("🎵 MP3")
        self.btn_video.clicked.connect(lambda: self.set_mode("video"))
        self.btn_audio.clicked.connect(lambda: self.set_mode("audio"))
        format_layout.addWidget(self.btn_video)
        format_layout.addWidget(self.btn_audio)

        # Quality
        quality_layout = QHBoxLayout()
        self.quality_label = QLabel("Qualidade:")
        self.quality_box = QComboBox()
        self.quality_box.addItem("Auto")
        quality_layout.addWidget(self.quality_label)
        quality_layout.addWidget(self.quality_box)

        # Folder selection
        path_layout = QHBoxLayout()
        self.path_label = QLabel("Local de salvamento:")
        self.path_btn = QPushButton("📁 Escolher pasta")
        self.path_btn.clicked.connect(self.select_folder)
        self.path_display = QLabel("")
        self.path_display.setStyleSheet("color: #00D2FF; font-size: 9pt;")
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_btn)
        path_layout.addWidget(self.path_display)

        # Progress
        self.progress = QProgressBar()

        # Download button
        self.download_btn = QPushButton("⬇️ Iniciar Download")
        self.download_btn.clicked.connect(self.start_download)

        # Add to layout
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

        # 🔥 Carrega pasta padrão salva nas configurações
        self.load_default_folder()

    # -----------------------------
    # PREVIEW (agora com tamanho)
    # -----------------------------
    def load_preview(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Aviso", "Insira um link válido.")
            return

        try:
            info = Downloader.get_video_info(url)
            self.current_video_info = info

            duration = info["duration"]
            minutes = duration // 60 if duration else 0
            hours = minutes // 60 if minutes >= 60 else 0
            duration_text = f"{hours}h {minutes % 60}min" if hours > 0 else f"{minutes} min"

            # Monta texto com tamanho se disponível
            size_text = f"💾 {info['filesize_mb']} MB" if info.get("filesize_mb") else "💾 Tamanho não disponível"

            self.video_info_label.setText(
                f"🎬 {info['title']}\n"
                f"👤 {info['uploader']}\n"
                f"⏱ {duration_text}  |  {size_text}"
            )

            if info.get("thumbnail"):
                response = requests.get(info["thumbnail"], timeout=5)
                image = QPixmap()
                image.loadFromData(response.content)
                self.thumbnail_label.setPixmap(
                    image.scaled(320, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )

            self.quality_box.clear()
            self.quality_box.addItem("Auto")
            if info.get("qualities"):
                self.quality_box.addItems(info["qualities"])

            QMessageBox.information(self, "Sucesso", f"Vídeo validado!\n\nTítulo: {info['title']}")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar informações:\n{str(e)}")

    # -----------------------------
    # CONTROLES DE MODO
    # -----------------------------
    def set_mode(self, mode):
        self.mode = mode
        self.update_button_styles()
        if mode == "video":
            self.quality_label.setText("Qualidade do vídeo:")
        else:
            self.quality_label.setText("Qualidade do áudio:")
            self.quality_box.setCurrentText("Auto")

    def update_button_styles(self):
        """Define estilos dos botões MP4/MP3 baseado no tema atual (Dark/Light)."""
        app = QApplication.instance()
        bg_color = app.palette().window().color()
        is_dark = bg_color.lightness() < 128

        if self.mode == "video":
            self.btn_video.setStyleSheet("""
                background-color: #00C853;
                color: black;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
            """)
            if is_dark:
                self.btn_audio.setStyleSheet("""
                    background-color: #2A2F3A;
                    color: #E6E6E6;
                    border: 1px solid #3A3F4A;
                    border-radius: 8px;
                    padding: 10px;
                """)
            else:
                self.btn_audio.setStyleSheet("""
                    background-color: #F0F2F5;
                    color: #1F2A3E;
                    border: 1px solid #D0D7DE;
                    border-radius: 8px;
                    padding: 10px;
                """)
        else:
            self.btn_audio.setStyleSheet("""
                background-color: #00C853;
                color: black;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
            """)
            if is_dark:
                self.btn_video.setStyleSheet("""
                    background-color: #2A2F3A;
                    color: #E6E6E6;
                    border: 1px solid #3A3F4A;
                    border-radius: 8px;
                    padding: 10px;
                """)
            else:
                self.btn_video.setStyleSheet("""
                    background-color: #F0F2F5;
                    color: #1F2A3E;
                    border: 1px solid #D0D7DE;
                    border-radius: 8px;
                    padding: 10px;
                """)

    def refresh_theme(self):
        self.update_button_styles()

    # -----------------------------
    # PASTA (com persistência)
    # -----------------------------
    def load_default_folder(self):
        """Carrega a pasta padrão das configurações (vídeo ou áudio)."""
        if self.mode == "video":
            default_path = Config.get_default_video_folder()
        else:
            default_path = Config.get_default_audio_folder()

        if os.path.exists(default_path):
            self.folder_path = default_path
            self.path_display.setText(f"📁 Pasta padrão: {default_path}")
        else:
            self.folder_path = None
            self.path_display.setText("")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Escolher pasta de destino")
        if folder:
            self.folder_path = folder
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

        selected_quality = self.quality_box.currentText()
        if selected_quality == "Auto":
            selected_quality = None

        output_path = self.folder_path if self.folder_path else None
        self.worker = DownloadWorker(url, self.mode, selected_quality, output_path)

        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_download_finished)
        self.worker.error.connect(self.on_download_error)

        self.worker.start()

    def on_download_finished(self, message):
        QMessageBox.information(self, "✅ Download concluído", message)
        self.reset_ui()

    def on_download_error(self, error_message):
        QMessageBox.critical(self, "❌ Erro no download", error_message)
        self.reset_ui()

    def reset_ui(self):
        self.download_btn.setEnabled(True)
        self.progress.setValue(0)