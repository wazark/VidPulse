from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("🎬 VidPulse")
        title.setStyleSheet("font-size: 24pt; font-weight: bold;")
        layout.addWidget(title)

        desc = QLabel("Download de vídeos e áudio do YouTube de forma simples e rápida.")
        layout.addWidget(desc)

        version = QLabel("Versão: v0.3")
        layout.addWidget(version)

        features = QLabel(
            "Features:\n"
            "- Download MP4\n"
            "- Download MP3\n"
            "- Escolha de qualidade\n"
            "- Tema Dark/Light"
        )
        layout.addWidget(features)

        # 🔥 Espaço que empurra o footer para baixo
        layout.addStretch()

        footer = QLabel(
            "© Orbytek\n"
            "Desenvolvido por Diony da Silva Costa\n"
            "Fundador da Orbytek\n\n"
            "Projeto educacional criado para apoiar\n"
            "os alunos da SharkCoders Aveiro."
        )
        footer.setStyleSheet("font-size: 10pt; color: gray;")
        footer.setAlignment(Qt.AlignLeft)

        layout.addWidget(footer)

        self.setLayout(layout)