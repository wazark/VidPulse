import os
import sys


class ThemeManager:

    @staticmethod
    def get_base_path():
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
        return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    @staticmethod
    def load_theme(app, theme="dark"):
        base_path = ThemeManager.get_base_path()

        # 🔥 TESTA MÚLTIPLOS CAMINHOS (robusto)
        possible_paths = [
            os.path.join(base_path, "ui", "styles", f"{theme}.qss"),
            os.path.join(base_path, "styles", f"{theme}.qss"),
            os.path.join(os.getcwd(), "ui", "styles", f"{theme}.qss"),
        ]

        style_path = None

        for path in possible_paths:
            if os.path.exists(path):
                style_path = path
                break

        if not style_path:
            raise FileNotFoundError(f"QSS não encontrado. Caminhos testados: {possible_paths}")

        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())