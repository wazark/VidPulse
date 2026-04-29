import os
import sys

class ThemeManager:

    @staticmethod
    def get_base_path():
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
        return os.path.dirname(os.path.dirname(__file__))

    @staticmethod
    def load_theme(app, theme="dark"):
        base_path = ThemeManager.get_base_path()

        # 🔥 CORREÇÃO AQUI (remover "ui")
        style_path = os.path.join(base_path, "styles", f"{theme}.qss")

        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())