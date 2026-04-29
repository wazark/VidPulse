from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QProgressBar,
    QFileDialog, QComboBox, QLabel, QMessageBox, QApplication, QMenu
)
from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QPixmap, QDesktopServices
import os
import requests

from ui.download_worker import DownloadWorker
from core.downloader import Downloader
from core.config import Config


class DownloaderPage(QWidget):
    open_settings_signal = Signal()  # 🔥 Sinal para abrir configurações completas

    def __init__(self):
        super().__init__()

        self.mode = Config.get_default_format()  # 'video' ou 'audio'
        self.folder_path = None
        self.worker = None
        self.current_video_info = None

        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Cabeçalho com título e botão de configuração
        header_layout = QHBoxLayout()
        title_label = QLabel("📥 Downloader")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Botão de engrenagem com menu popup
        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setFixedSize(36, 36)
        self.settings_btn.setToolTip("Configurações rápidas")
        self.settings_menu = QMenu(self)
        self.quality_menu = self.settings_menu.addMenu("Qualidade padrão")
        self.format_menu = self.settings_menu.addMenu("Formato padrão")
        self.settings_menu.addSeparator()
        self.settings_menu.addAction("Abrir configurações completas", self.open_full_settings)

        # Preenche submenu de qualidade
        self.quality_actions = {}
        for q in ["Auto", "2160p", "1440p", "1080p", "720p", "480p", "360p"]:
            action = self.quality_menu.addAction(q)
            action.triggered.connect(lambda checked, qual=q: self.set_default_quality(qual))
            self.quality_actions[q] = action

        # Preenche submenu de formato
        self.format_actions = {}
        for fmt, label in [("video", "🎬 MP4"), ("audio", "🎵 MP3")]:
            action = self.format_menu.addAction(label)
            action.triggered.connect(lambda checked, f=fmt: self.set_default_format(f))
            self.format_actions[fmt] = action

        self.settings_btn.setMenu(self.settings_menu)
        header_layout.addWidget(self.settings_btn)
        main_layout.addLayout(header_layout)

        # URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Cole o link do vídeo do YouTube")

        self.preview_btn = QPushButton("🔍 Validar vídeo")
        self.preview_btn.clicked.connect(self.load_preview)

        self.video_info_label = QLabel("")
        self.video_info_label.setStyleSheet("color: #7A7E8F; font-size: 10pt;")
        self.video_info_label.setWordWrap(True)

        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedHeight(180)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)

        # Formatos
        format_layout = QHBoxLayout()
        self.btn_video = QPushButton("🎬 VÍDEO")
        self.btn_audio = QPushButton("🎵 ÁUDIO")
        self.btn_video.clicked.connect(lambda: self.set_mode("video"))
        self.btn_audio.clicked.connect(lambda: self.set_mode("audio"))
        format_layout.addWidget(self.btn_video)
        format_layout.addWidget(self.btn_audio)

        # Qualidade
        quality_layout = QHBoxLayout()
        self.quality_label = QLabel("Qualidade:")
        self.quality_box = QComboBox()
        self.quality_box.addItem("Auto")
        quality_layout.addWidget(self.quality_label)
        quality_layout.addWidget(self.quality_box)

        # Pasta
        path_layout = QHBoxLayout()
        self.path_label = QLabel("Local de salvamento:")
        self.path_btn = QPushButton("📁 Escolher pasta")
        self.path_btn.clicked.connect(self.select_folder)
        self.path_display = QLabel("")
        self.path_display.setStyleSheet("color: #00D2FF; font-size: 9pt;")
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_btn)
        path_layout.addWidget(self.path_display)

        # Progresso + ETA + Cancelar
        progress_layout = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setFormat("%p%")
        self.eta_label = QLabel("")
        self.eta_label.setStyleSheet("color: #7A7E8F; font-size: 9pt;")
        self.eta_label.setMinimumWidth(80)
        self.cancel_btn = QPushButton("⏹️ Cancelar")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_download)
        progress_layout.addWidget(self.progress, 4)
        progress_layout.addWidget(self.eta_label)
        progress_layout.addWidget(self.cancel_btn)

        # Download
        self.download_btn = QPushButton("⬇️ Iniciar Download")
        self.download_btn.clicked.connect(self.start_download)

        # Montagem
        main_layout.addWidget(self.url_input)
        main_layout.addWidget(self.preview_btn)
        main_layout.addWidget(self.video_info_label)
        main_layout.addWidget(self.thumbnail_label)
        main_layout.addLayout(format_layout)
        main_layout.addLayout(quality_layout)
        main_layout.addLayout(path_layout)
        main_layout.addLayout(progress_layout)
        main_layout.addWidget(self.download_btn)

        self.setLayout(main_layout)

        # Carrega configurações salvas
        self.load_saved_settings()
        self.update_button_styles()
        self.load_default_folder()

    # -----------------------------
    # CONFIGURAÇÕES RÁPIDAS
    # -----------------------------
    def load_saved_settings(self):
        default_format = Config.get_default_format()
        self.set_mode(default_format)

        self.default_quality = Config.get_default_quality()
        for q, action in self.quality_actions.items():
            action.setChecked(q == self.default_quality)

        for fmt, action in self.format_actions.items():
            action.setChecked(fmt == default_format)

    def set_default_quality(self, quality):
        Config.set_default_quality(quality)
        self.default_quality = quality
        if self.quality_box.count() > 0:
            idx = self.quality_box.findText(quality)
            if idx >= 0:
                self.quality_box.setCurrentIndex(idx)
            elif quality == "Auto":
                self.quality_box.setCurrentIndex(0)

    def set_default_format(self, fmt):
        Config.set_default_format(fmt)
        self.set_mode(fmt)

    def open_full_settings(self):
        """Abre a página de configurações completas."""
        self.open_settings_signal.emit()

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
            self.current_video_info = info

            duration = info["duration"]
            minutes = duration // 60 if duration else 0
            hours = minutes // 60 if minutes >= 60 else 0
            duration_text = f"{hours}h {minutes % 60}min" if hours > 0 else f"{minutes} min"

            size_text = f"💾 {info['filesize_mb']} MB" if info.get("filesize_mb") else "💾 Tamanho não disponível"

            self.video_info_label.setText(
                f"🎬 {info['title']}\n👤 {info['uploader']}\n⏱ {duration_text}  |  {size_text}"
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
                if self.default_quality in info["qualities"]:
                    self.quality_box.setCurrentText(self.default_quality)
                elif self.default_quality == "Auto":
                    self.quality_box.setCurrentIndex(0)

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
        self.load_default_folder()

    def update_button_styles(self):
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
    # PASTA
    # -----------------------------
    def load_default_folder(self):
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
        self.preview_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress.setValue(0)
        self.eta_label.setText("")

        selected_quality = self.quality_box.currentText()
        if selected_quality == "Auto":
            selected_quality = None

        output_path = self.folder_path if self.folder_path else None
        self.worker = DownloadWorker(url, self.mode, selected_quality, output_path)

        self.worker.progress.connect(self.progress.setValue)
        self.worker.eta.connect(self.eta_label.setText)
        self.worker.finished.connect(self.on_download_finished)
        self.worker.error.connect(self.on_download_error)

        self.worker.start()

    def cancel_download(self):
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.cancel_btn.setEnabled(False)
            self.eta_label.setText("Cancelando...")

    def on_download_finished(self, message, file_path):
        self.download_btn.setEnabled(True)
        self.preview_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Download concluído")
        msg_box.setText(f"{message}\n\nFicheiro guardado em:\n{file_path}")
        msg_box.setIcon(QMessageBox.Information)
        open_btn = msg_box.addButton("📂 Abrir pasta", QMessageBox.ActionRole)
        ok_btn = msg_box.addButton("OK", QMessageBox.AcceptRole)
        msg_box.exec()

        if msg_box.clickedButton() == open_btn:
            folder = os.path.dirname(file_path)
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder))
        self.reset_ui()

    def on_download_error(self, error_message):
        self.download_btn.setEnabled(True)
        self.preview_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        QMessageBox.critical(self, "❌ Erro no download", error_message)
        self.reset_ui()

    def reset_ui(self):
        self.progress.setValue(0)
        self.eta_label.setText("")
        self.download_btn.setEnabled(True)
        self.preview_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)