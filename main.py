import sys
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.widgets.theme_manager import ThemeManager
from core.config import Config  # 🔥 Carregar configurações

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Carrega o tema salvo
    saved_theme = Config.get_theme()
    ThemeManager.load_theme(app, saved_theme)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())