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

        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14pt;")

        content_label = QLabel(content)
        content_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(content_label)

        self.setLayout(layout)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # 🔥 HEADER
        title = QLabel("🎬 VidPulse")
        title.setStyleSheet("font-size: 26pt; font-weight: bold;")

        subtitle = QLabel("Download de vídeos e áudio do YouTube de forma simples, rápida e moderna.")
        subtitle.setStyleSheet("color: gray;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # 🔥 CARDS (linha 1)
        cards_layout = QHBoxLayout()

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

        cards_layout.addWidget(features_card)
        cards_layout.addWidget(about_card)

        # 🔥 CARD versão
        version_card = Card(
            "🧪 Estado do Projeto",
            "Versão atual: v0.3\n\n"
            "Aplicação em desenvolvimento contínuo com melhorias de UI, "
            "performance e novas funcionalidades."
        )

        # 🔥 FOOTER
        footer = QLabel(
            "© Orbytek • Diony da Silva Costa\n"
            "Fundador da Orbytek\n"
            "Projeto educacional para alunos da SharkCoders Aveiro"
        )
        footer.setStyleSheet("font-size: 10pt; color: gray;")
        footer.setAlignment(Qt.AlignLeft)

        # 🔥 BUILD FINAL
        main_layout.addSpacing(10)
        main_layout.addLayout(cards_layout)
        main_layout.addWidget(version_card)

        main_layout.addStretch()
        main_layout.addWidget(footer)

        self.setLayout(main_layout)