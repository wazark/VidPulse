from PySide6.QtGui import QIcon
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
        self.resize(900, 500)

        # 🔥 ÍCONE CORRIGIDO
        icon_path = os.path.join(self.get_base_path(), "assets", "icon.png")
        self.setWindowIcon(QIcon(icon_path))

        main_layout = QHBoxLayout()

        # SIDEBAR
        sidebar = QVBoxLayout()

        logo = QLabel("🎬 VidPulse")
        logo.setStyleSheet("font-size: 18pt; font-weight: bold; margin-bottom: 20px;")
        sidebar.addWidget(logo)

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

        # AÇÕES
        btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_download.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_settings.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        # FINAL
        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.stack, 4)

        self.setLayout(main_layout)

    # 🔥 MÉTODO CORRIGIDO
    def get_base_path(self):
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
        return os.path.dirname(os.path.dirname(__file__))

    def change_theme(self, theme):
        from PySide6.QtWidgets import QApplication
        ThemeManager.load_theme(QApplication.instance(), theme)