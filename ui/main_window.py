from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
import os
import sys

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel
)

from ui.pages.home_page import HomePage
from ui.pages.downloader_page import DownloaderPage
from ui.pages.settings_page import SettingsPage
from ui.widgets.theme_manager import ThemeManager


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VidPulse — Download de Vídeo e Áudio")
        self.resize(1100, 660)

        # Carregar ícone da janela (tenta .png e .ico)
        icon_path = self.get_icon_path()
        if icon_path and os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            # Se não encontrar, tenta apenas definir um ícone vazio (evita o ícone padrão do Qt)
            self.setWindowIcon(QIcon())

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # SIDEBAR
        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(20, 20, 20, 20)
        sidebar.setSpacing(16)

        # Logo
        logo_path = self.get_logo_path()
        logo_label = QLabel()
        if logo_path and os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            logo_pixmap = logo_pixmap.scaledToWidth(150, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("🎬 VidPulse")
            logo_label.setStyleSheet("font-size: 22pt; font-weight: bold;")
        logo_label.setAlignment(Qt.AlignCenter)
        sidebar.addWidget(logo_label)

        btn_home = QPushButton("🏠 Home")
        btn_download = QPushButton("⬇️ Downloader")
        btn_settings = QPushButton("⚙️ Configurações")

        sidebar.addWidget(btn_home)
        sidebar.addWidget(btn_download)
        sidebar.addStretch()
        sidebar.addWidget(btn_settings)

        # STACK
        self.stack = QStackedWidget()
        self.home_page = HomePage()
        self.downloader_page = DownloaderPage()
        self.settings_page = SettingsPage(self.change_theme)

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.downloader_page)
        self.stack.addWidget(self.settings_page)

        # Conecta o sinal do downloader para abrir configurações
        self.downloader_page.open_settings_signal.connect(lambda: self.stack.setCurrentIndex(2))

        btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_download.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_settings.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setMaximumWidth(220)
        sidebar_widget.setObjectName("sidebar")

        main_layout.addWidget(sidebar_widget, 1)
        main_layout.addWidget(self.stack, 4)
        self.setLayout(main_layout)

    def get_base_path(self):
        """Retorna o caminho base do projecto (raiz)."""
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
        return os.path.dirname(os.path.dirname(__file__))

    def get_icon_path(self):
        """Tenta encontrar o ícone da janela (icon.png ou icon.ico)."""
        base = self.get_base_path()
        candidates = [
            os.path.join(base, "assets", "icon.png"),
            os.path.join(base, "assets", "icon.ico"),
            os.path.join(base, "assets", "Icon.png"),
            os.path.join(base, "assets", "Icon.ico"),
        ]
        for cand in candidates:
            if os.path.exists(cand):
                return cand
        return None

    def get_logo_path(self):
        """Retorna o caminho para o logótipo VidPulse.png."""
        base = self.get_base_path()
        logo = os.path.join(base, "assets", "VidPulse.png")
        if os.path.exists(logo):
            return logo
        return None

    def change_theme(self, theme):
        from PySide6.QtWidgets import QApplication
        ThemeManager.load_theme(QApplication.instance(), theme)
        self.downloader_page.refresh_theme()