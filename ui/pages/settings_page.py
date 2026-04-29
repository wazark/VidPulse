from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QFileDialog, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Qt
import shutil
import os

from core.config import Config  # 🔥 Gestão de configurações


class SettingsPage(QWidget):
    def __init__(self, theme_callback):
        super().__init__()
        self.theme_callback = theme_callback

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # ---------- TEMA ----------
        layout.addWidget(QLabel("🎨 Tema da aplicação:"))
        self.theme_box = QComboBox()
        self.theme_box.addItems(["Dark", "Light"])
        layout.addWidget(self.theme_box)

        apply_btn = QPushButton("✨ Aplicar tema")
        apply_btn.clicked.connect(self.save_and_apply_theme)
        layout.addWidget(apply_btn)

        layout.addWidget(QLabel(""))

        # ---------- PASTAS PADRÃO ----------
        layout.addWidget(QLabel("📁 Pastas padrão:"))

        # Pasta para vídeos
        video_folder_layout = QHBoxLayout()
        video_folder_layout.addWidget(QLabel("Vídeos:"))
        self.video_folder_display = QLabel(Config.get_default_video_folder())
        self.video_folder_display.setStyleSheet("color: #7A7E8F;")
        video_folder_btn = QPushButton("Alterar")
        video_folder_btn.clicked.connect(lambda: self.change_default_folder("video"))
        video_folder_layout.addWidget(self.video_folder_display)
        video_folder_layout.addWidget(video_folder_btn)
        layout.addLayout(video_folder_layout)

        # Pasta para áudio
        audio_folder_layout = QHBoxLayout()
        audio_folder_layout.addWidget(QLabel("Áudio:"))
        self.audio_folder_display = QLabel(Config.get_default_audio_folder())
        self.audio_folder_display.setStyleSheet("color: #7A7E8F;")
        audio_folder_btn = QPushButton("Alterar")
        audio_folder_btn.clicked.connect(lambda: self.change_default_folder("audio"))
        audio_folder_layout.addWidget(self.audio_folder_display)
        audio_folder_layout.addWidget(audio_folder_btn)
        layout.addLayout(audio_folder_layout)

        layout.addWidget(QLabel(""))

        # ---------- IDIOMA ----------
        layout.addWidget(QLabel("🌐 Idioma:"))
        self.lang_box = QComboBox()
        self.lang_box.addItems(["Português", "English", "Español", "Deutsch", "Français"])
        self.lang_box.setCurrentText(Config.get_language())  # carrega salvo
        self.lang_box.currentTextChanged.connect(self.save_language)
        layout.addWidget(self.lang_box)

        layout.addWidget(QLabel(""))

        # ---------- COOKIES ----------
        layout.addWidget(QLabel("🍪 Cookies (para vídeos restritos/idade):"))
        cookie_layout = QVBoxLayout()
        self.cookie_status = QLabel("📄 Status: Nenhum arquivo de cookies carregado")
        self.cookie_status.setStyleSheet("color: #ff9800; font-size: 10pt;")
        cookie_btn = QPushButton("📁 Carregar arquivo cookies.txt")
        cookie_btn.clicked.connect(self.load_cookies)
        remove_cookie_btn = QPushButton("🗑️ Remover cookies")
        remove_cookie_btn.clicked.connect(self.remove_cookies)
        cookie_layout.addWidget(self.cookie_status)
        cookie_layout.addWidget(cookie_btn)
        cookie_layout.addWidget(remove_cookie_btn)
        layout.addLayout(cookie_layout)

        layout.addWidget(QLabel(""))
        help_cookies_btn = QPushButton("ℹ️ Como obter cookies.txt")
        help_cookies_btn.clicked.connect(self.show_cookie_help)
        layout.addWidget(help_cookies_btn)

        layout.addWidget(QLabel(""))

        # ---------- AJUDA GERAL ----------
        help_btn = QPushButton("❓ Ajuda geral")
        help_btn.clicked.connect(self.show_help)
        layout.addWidget(help_btn)

        layout.addStretch()
        self.setLayout(layout)

        # Carrega estado atual dos cookies
        self.check_cookie_status()
        # Carrega o tema salvo no combo box
        self.load_saved_theme()

    # ---------- Tema ----------
    def load_saved_theme(self):
        """Sincroniza o combo box com o tema salvo."""
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

    # ---------- Idioma ----------
    def save_language(self, lang):
        Config.set_language(lang)
        # Aqui futuramente pode-se aplicar traduções dinâmicas

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
            "3. Escolha MP4 ou MP3\n"
            "4. Defina qualidade\n"
            "5. Escolha a pasta\n"
            "6. Clique em Download\n\n"
            "🍪 **Vídeos com restrição:** use cookies.\n"
            "⚙️ **Configurações:** tema e pastas padrão são salvos automaticamente."
        )