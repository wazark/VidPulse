from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame
)
from PySide6.QtCore import Qt


class Card(QFrame):
    def __init__(self, title, content):
        super().__init__()
        self.setObjectName("card")
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 15pt;")
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("line-height: 1.4; color: #7A7E8F;")

        layout.addWidget(title_label)
        layout.addWidget(content_label)
        self.setLayout(layout)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Cabeçalho
        title = QLabel("🎬 VidPulse")
        title.setStyleSheet("font-size: 32pt; font-weight: bold;")
        subtitle = QLabel("Download de vídeos e áudio do YouTube de forma simples, rápida e moderna.")
        subtitle.setStyleSheet("color: #7A7E8F; font-size: 12pt;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(20)

        # Cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        features_card = Card(
            "🚀 Funcionalidades",
            "• Download de vídeos em MP4\n"
            "• Conversão para MP3\n"
            "• Escolha de qualidade\n"
            "• Interface moderna\n"
            "• Tema Dark e Light"
        )

        about_card = Card(
            "📚 Sobre o Projeto",
            "VidPulse é uma ferramenta educacional criada para auxiliar alunos "
            "no processo de aprendizagem de desenvolvimento de software e automação."
        )

        version_card = Card(
            "🧪 Estado do Projeto",
            "Versão atual: v1.0\n\n"
            "Aplicação em desenvolvimento contínuo com melhorias de UI, "
            "performance e novas funcionalidades."
        )

        cards_layout.addWidget(features_card)
        cards_layout.addWidget(about_card)

        main_layout.addLayout(cards_layout)
        main_layout.addWidget(version_card)
        main_layout.addStretch()

        # Footer
        footer = QLabel(
            "© Orbytek • Diony da Silva Costa\n"
            "Projeto educacional para alunos da SharkCoders Aveiro"
        )
        footer.setStyleSheet("font-size: 10pt; color: #7A7E8F;")
        footer.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)