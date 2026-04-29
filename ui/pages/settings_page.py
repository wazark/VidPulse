from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton


class SettingsPage(QWidget):
    def __init__(self, theme_callback):
        super().__init__()

        layout = QVBoxLayout()

        # Tema
        layout.addWidget(QLabel("Tema da aplicação:"))

        self.theme_box = QComboBox()
        self.theme_box.addItems(["Dark", "Light"])
        layout.addWidget(self.theme_box)

        apply_btn = QPushButton("Aplicar tema")
        apply_btn.clicked.connect(lambda: theme_callback(self.theme_box.currentText().lower()))
        layout.addWidget(apply_btn)

        # Idioma
        layout.addWidget(QLabel("Idioma:"))

        self.lang_box = QComboBox()
        self.lang_box.addItems(["Português", "English", "Español", "Deutsch", "Français"])
        layout.addWidget(self.lang_box)

        # Ajuda
        help_btn = QPushButton("❓ Ajuda")
        help_btn.clicked.connect(self.show_help)
        layout.addWidget(help_btn)

        layout.addStretch()

        self.setLayout(layout)

    def show_help(self):
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.information(
            self,
            "Ajuda",
            "1. Cole o link do YouTube\n"
            "2. Escolha MP4 ou MP3\n"
            "3. Defina qualidade\n"
            "4. Escolha a pasta\n"
            "5. Clique em Download"
        )