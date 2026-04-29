import os

class ThemeManager:

    @staticmethod
    def load_theme(app, theme="dark"):
        base_path = os.path.dirname(os.path.dirname(__file__))
        style_path = os.path.join(base_path, "styles", f"{theme}.qss")

        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())