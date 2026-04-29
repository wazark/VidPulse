from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
import shutil
import os


class SettingsPage(QWidget):
    def __init__(self, theme_callback):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Tema
        layout.addWidget(QLabel("🎨 Tema da aplicação:"))
        self.theme_box = QComboBox()
        self.theme_box.addItems(["Dark", "Light"])
        layout.addWidget(self.theme_box)

        apply_btn = QPushButton("✨ Aplicar tema")
        apply_btn.clicked.connect(lambda: theme_callback(self.theme_box.currentText().lower()))
        layout.addWidget(apply_btn)

        layout.addWidget(QLabel(""))

        # 🔥 COOKIES (NOVO)
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

        # Como obter cookies
        help_cookies_btn = QPushButton("ℹ️ Como obter cookies.txt")
        help_cookies_btn.clicked.connect(self.show_cookie_help)
        layout.addWidget(help_cookies_btn)

        layout.addWidget(QLabel(""))

        # Idioma
        layout.addWidget(QLabel("🌐 Idioma:"))
        self.lang_box = QComboBox()
        self.lang_box.addItems(["Português", "English", "Español", "Deutsch", "Français"])
        layout.addWidget(self.lang_box)

        layout.addWidget(QLabel(""))

        # Ajuda geral
        help_btn = QPushButton("❓ Ajuda geral")
        help_btn.clicked.connect(self.show_help)
        layout.addWidget(help_btn)

        layout.addStretch()

        self.setLayout(layout)

        # Verifica se já existe cookie
        self.check_cookie_status()

    def check_cookie_status(self):
        """Verifica se já existe um arquivo de cookies"""
        from core.downloader import Downloader
        cookie_file = Downloader.get_cookie_file()

        if cookie_file and os.path.exists(cookie_file):
            self.cookie_status.setText(f"✅ Status: Cookies carregados ({cookie_file})")
            self.cookie_status.setStyleSheet("color: #00c853; font-size: 10pt;")
        else:
            self.cookie_status.setText("⚠️ Status: Nenhum arquivo de cookies. Vídeos com restrição podem falhar.")
            self.cookie_status.setStyleSheet("color: #ff9800; font-size: 10pt;")

    def load_cookies(self):
        """Carrega arquivo de cookies"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo cookies.txt",
            "",
            "Arquivos de cookies (*.txt);;Todos os arquivos (*)"
        )

        if file_path:
            # Cria diretório .vidpulse no usuário
            user_cookie_dir = os.path.join(os.path.expanduser("~"), ".vidpulse")
            os.makedirs(user_cookie_dir, exist_ok=True)

            destination = os.path.join(user_cookie_dir, "cookies.txt")

            try:
                shutil.copy2(file_path, destination)
                QMessageBox.information(
                    self,
                    "Sucesso",
                    "✅ Arquivo de cookies instalado com sucesso!\n\n"
                    "Agora você pode baixar vídeos com restrição de idade e região."
                )
                self.check_cookie_status()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"❌ Falha ao copiar arquivo: {str(e)}")

    def remove_cookies(self):
        """Remove arquivo de cookies"""
        user_cookie_file = os.path.join(os.path.expanduser("~"), ".vidpulse", "cookies.txt")

        if os.path.exists(user_cookie_file):
            os.remove(user_cookie_file)
            QMessageBox.information(self, "Sucesso", "✅ Cookies removidos com sucesso!")
            self.check_cookie_status()
        else:
            QMessageBox.information(self, "Info", "Nenhum arquivo de cookies encontrado.")

    def show_cookie_help(self):
        """Mostra ajuda sobre como obter cookies"""
        QMessageBox.information(
            self,
            "🍪 Como obter cookies.txt",
            "1. Instale a extensão 'Get cookies.txt' no seu navegador:\n"
            "   - Chrome: 'Get cookies.txt LOCALLY'\n"
            "   - Firefox: 'cookies.txt'\n\n"
            "2. Faça login no YouTube pelo navegador\n\n"
            "3. Clique na extensão e exporte os cookies\n\n"
            "4. Salve como 'cookies.txt'\n\n"
            "5. Use o botão 'Carregar arquivo cookies.txt' acima\n\n"
            "⚠️ Atenção: Não compartilhe seu arquivo de cookies com ninguém!"
        )

    def show_help(self):
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.information(
            self,
            "📖 Ajuda do VidPulse",
            "🎬 **Download de Vídeos:**\n"
            "1. Cole o link do YouTube\n"
            "2. Clique em 'Validar vídeo'\n"
            "3. Escolha MP4 ou MP3\n"
            "4. Defina qualidade\n"
            "5. Escolha a pasta\n"
            "6. Clique em Download\n\n"
            "🍪 **Vídeos com restrição:**\n"
            "• Use a aba 'Cookies' acima\n"
            "• Exporte cookies do navegador\n"
            "• Carregue o arquivo no app\n\n"
            "❓ **Problemas comuns:**\n"
            "• Vídeo privado/removido\n"
            "• Restrição geográfica\n"
            "• Exige autenticação (use cookies)"
        )