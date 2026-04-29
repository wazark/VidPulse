from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QFileDialog, QMessageBox, QTabWidget,
    QCheckBox, QSpinBox
)
from PySide6.QtCore import Qt
import shutil
import os

from core.config import Config


class SettingsPage(QWidget):
    def __init__(self, theme_callback):
        super().__init__()
        self.theme_callback = theme_callback

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # -------------------- ABA APARÊNCIA --------------------
        tab_appearance = QWidget()
        appearance_layout = QVBoxLayout()
        appearance_layout.setSpacing(15)

        appearance_layout.addWidget(QLabel("🎨 Tema da aplicação:"))
        self.theme_box = QComboBox()
        self.theme_box.addItems(["Dark", "Light"])
        appearance_layout.addWidget(self.theme_box)

        apply_btn = QPushButton("✨ Aplicar tema")
        apply_btn.clicked.connect(self.save_and_apply_theme)
        appearance_layout.addWidget(apply_btn)

        appearance_layout.addStretch()
        tab_appearance.setLayout(appearance_layout)
        self.tabs.addTab(tab_appearance, "Aparência")

        # -------------------- ABA DOWNLOADS (MODIFICADA) --------------------
        tab_downloads = QWidget()
        downloads_layout = QVBoxLayout()
        downloads_layout.setSpacing(15)

        downloads_layout.addWidget(QLabel("📁 Pastas padrão:"))
        # Pasta vídeos
        vid_layout = QHBoxLayout()
        vid_layout.addWidget(QLabel("Vídeos:"))
        self.video_folder_display = QLabel(Config.get_default_video_folder())
        self.video_folder_display.setStyleSheet("color: #7A7E8F;")
        vid_btn = QPushButton("Alterar")
        vid_btn.clicked.connect(lambda: self.change_default_folder("video"))
        vid_layout.addWidget(self.video_folder_display)
        vid_layout.addWidget(vid_btn)
        downloads_layout.addLayout(vid_layout)

        # Pasta áudio
        aud_layout = QHBoxLayout()
        aud_layout.addWidget(QLabel("Áudio:"))
        self.audio_folder_display = QLabel(Config.get_default_audio_folder())
        self.audio_folder_display.setStyleSheet("color: #7A7E8F;")
        aud_btn = QPushButton("Alterar")
        aud_btn.clicked.connect(lambda: self.change_default_folder("audio"))
        aud_layout.addWidget(self.audio_folder_display)
        aud_layout.addWidget(aud_btn)
        downloads_layout.addLayout(aud_layout)

        downloads_layout.addWidget(QLabel(""))
        downloads_layout.addWidget(QLabel("⚙️ Qualidade padrão:"))
        self.default_quality_combo = QComboBox()
        self.default_quality_combo.addItems(["Auto", "2160p", "1440p", "1080p", "720p", "480p", "360p"])
        self.default_quality_combo.setCurrentText(Config.get_default_quality())
        self.default_quality_combo.currentTextChanged.connect(Config.set_default_quality)
        downloads_layout.addWidget(self.default_quality_combo)

        # 🔥 Modo padrão (MP4 ou MP3)
        downloads_layout.addWidget(QLabel("🎬 Modo padrão:"))
        self.default_mode_combo = QComboBox()
        self.default_mode_combo.addItems(["MP4 (Vídeo)", "MP3 (Áudio)"])
        current_mode = Config.get_default_format()
        self.default_mode_combo.setCurrentIndex(0 if current_mode == "video" else 1)
        self.default_mode_combo.currentIndexChanged.connect(self.on_default_mode_changed)
        downloads_layout.addWidget(self.default_mode_combo)

        downloads_layout.addWidget(QLabel(""))  # espaçamento

        # 🔥 Formato de vídeo
        downloads_layout.addWidget(QLabel("🎬 Formato de vídeo:"))
        self.video_format_combo = QComboBox()
        self.video_format_combo.addItems(["mp4", "webm", "mkv"])
        self.video_format_combo.setCurrentText(Config.get_default_video_format())
        self.video_format_combo.currentTextChanged.connect(Config.set_default_video_format)
        downloads_layout.addWidget(self.video_format_combo)

        # 🔥 Formato de áudio
        downloads_layout.addWidget(QLabel("🎵 Formato de áudio:"))
        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(["mp3", "aac", "ogg", "m4a"])
        self.audio_format_combo.setCurrentText(Config.get_default_audio_format())
        self.audio_format_combo.currentTextChanged.connect(Config.set_default_audio_format)
        downloads_layout.addWidget(self.audio_format_combo)

        downloads_layout.addWidget(QLabel("📥 Downloads simultâneos (em breve):"))
        self.concurrent_spin = QSpinBox()
        self.concurrent_spin.setRange(1, 5)
        self.concurrent_spin.setValue(Config.get_max_concurrent_downloads())
        self.concurrent_spin.valueChanged.connect(Config.set_max_concurrent_downloads)
        downloads_layout.addWidget(self.concurrent_spin)

        downloads_layout.addStretch()
        tab_downloads.setLayout(downloads_layout)
        self.tabs.addTab(tab_downloads, "Downloads")

        # -------------------- ABA REDE --------------------
        tab_network = QWidget()
        network_layout = QVBoxLayout()
        network_layout.setSpacing(15)

        network_layout.addWidget(QLabel("🍪 Cookies (para vídeos restritos/idade):"))
        self.cookie_status = QLabel("📄 Status: Nenhum arquivo de cookies carregado")
        self.cookie_status.setStyleSheet("color: #ff9800; font-size: 10pt;")
        cookie_btn = QPushButton("📁 Carregar arquivo cookies.txt")
        cookie_btn.clicked.connect(self.load_cookies)
        remove_cookie_btn = QPushButton("🗑️ Remover cookies")
        remove_cookie_btn.clicked.connect(self.remove_cookies)
        network_layout.addWidget(self.cookie_status)
        network_layout.addWidget(cookie_btn)
        network_layout.addWidget(remove_cookie_btn)
        network_layout.addWidget(QLabel(""))
        help_cookies_btn = QPushButton("ℹ️ Como obter cookies.txt")
        help_cookies_btn.clicked.connect(self.show_cookie_help)
        network_layout.addWidget(help_cookies_btn)

        network_layout.addStretch()
        tab_network.setLayout(network_layout)
        self.tabs.addTab(tab_network, "Rede")

        # -------------------- ABA SISTEMA --------------------
        tab_system = QWidget()
        system_layout = QVBoxLayout()
        system_layout.setSpacing(15)

        system_layout.addWidget(QLabel("🌐 Idioma:"))
        self.lang_box = QComboBox()
        self.lang_box.addItems(["Português", "English", "Español", "Deutsch", "Français"])
        self.lang_box.setCurrentText(Config.get_language())
        self.lang_box.currentTextChanged.connect(Config.set_language)
        system_layout.addWidget(self.lang_box)

        system_layout.addWidget(QLabel(""))
        self.check_updates_cb = QCheckBox("Verificar atualizações ao iniciar")
        self.check_updates_cb.setChecked(Config.get_check_updates())
        self.check_updates_cb.toggled.connect(Config.set_check_updates)
        system_layout.addWidget(self.check_updates_cb)

        system_layout.addStretch()
        tab_system.setLayout(system_layout)
        self.tabs.addTab(tab_system, "Sistema")

        # Botão de ajuda geral (fora das tabs)
        help_btn = QPushButton("❓ Ajuda geral")
        help_btn.clicked.connect(self.show_help)

        layout.addWidget(self.tabs)
        layout.addWidget(help_btn)
        self.setLayout(layout)

        # Inicializa estados
        self.check_cookie_status()
        self.load_saved_theme()

    # ---------- Tema ----------
    def load_saved_theme(self):
        saved_theme = Config.get_theme()
        index = 0 if saved_theme == "dark" else 1
        self.theme_box.setCurrentIndex(index)

    def save_and_apply_theme(self):
        theme = self.theme_box.currentText().lower()
        Config.set_theme(theme)
        self.theme_callback(theme)

    # ---------- Pastas padrão ----------
    def change_default_folder(self, media_type):
        folder = QFileDialog.getExistingDirectory(self, f"Selecionar pasta padrão para {media_type}")
        if folder:
            if media_type == "video":
                Config.set_default_video_folder(folder)
                self.video_folder_display.setText(folder)
            else:
                Config.set_default_audio_folder(folder)
                self.audio_folder_display.setText(folder)
            QMessageBox.information(self, "Sucesso", f"Pasta padrão para {media_type} atualizada.")

    # ---------- Modo padrão (MP4/MP3) ----------
    def on_default_mode_changed(self, index):
        fmt = "video" if index == 0 else "audio"
        Config.set_default_format(fmt)

    # ---------- Cookies ----------
    def check_cookie_status(self):
        from core.downloader import Downloader
        cookie_file = Downloader.get_cookie_file()
        if cookie_file and os.path.exists(cookie_file):
            self.cookie_status.setText(f"✅ Status: Cookies carregados ({cookie_file})")
            self.cookie_status.setStyleSheet("color: #00c853; font-size: 10pt;")
        else:
            self.cookie_status.setText("⚠️ Status: Nenhum arquivo de cookies. Vídeos com restrição podem falhar.")
            self.cookie_status.setStyleSheet("color: #ff9800; font-size: 10pt;")

    def load_cookies(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar arquivo cookies.txt", "", "Arquivos de cookies (*.txt);;Todos os arquivos (*)"
        )
        if file_path:
            user_cookie_dir = os.path.join(os.path.expanduser("~"), ".vidpulse")
            os.makedirs(user_cookie_dir, exist_ok=True)
            destination = os.path.join(user_cookie_dir, "cookies.txt")
            try:
                shutil.copy2(file_path, destination)
                QMessageBox.information(self, "Sucesso", "✅ Arquivo de cookies instalado!")
                self.check_cookie_status()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"❌ Falha ao copiar arquivo: {str(e)}")

    def remove_cookies(self):
        user_cookie_file = os.path.join(os.path.expanduser("~"), ".vidpulse", "cookies.txt")
        if os.path.exists(user_cookie_file):
            os.remove(user_cookie_file)
            QMessageBox.information(self, "Sucesso", "✅ Cookies removidos!")
            self.check_cookie_status()
        else:
            QMessageBox.information(self, "Info", "Nenhum arquivo de cookies encontrado.")

    def show_cookie_help(self):
        QMessageBox.information(
            self, "🍪 Como obter cookies.txt",
            "1. Instale a extensão 'Get cookies.txt' no navegador.\n"
            "2. Faça login no YouTube.\n"
            "3. Exporte os cookies e salve como 'cookies.txt'.\n"
            "4. Use o botão 'Carregar arquivo cookies.txt'."
        )

    def show_help(self):
        QMessageBox.information(
            self, "📖 Ajuda do VidPulse",
            "🎬 **Download de Vídeos:**\n"
            "1. Cole o link do YouTube\n"
            "2. Clique em 'Validar vídeo'\n"
            "3. Escolha MP4 ou MP3 (formato real será o definido nas Configurações)\n"
            "4. Defina qualidade\n"
            "5. Escolha a pasta\n"
            "6. Clique em Download\n\n"
            "🍪 **Vídeos com restrição:** use cookies.\n"
            "⚙️ **Configurações:** tema, pastas, formatos de vídeo/áudio são salvos automaticamente."
        )