import sys
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.widgets.theme_manager import ThemeManager

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ThemeManager.load_theme(app, "dark")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())