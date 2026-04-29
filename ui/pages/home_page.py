from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QGridLayout
)
from PySide6.QtCore import Qt


class Card(QFrame):
    def __init__(self, title, content, emoji=""):
        super().__init__()
        self.setObjectName("card")
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Título com emoji
        title_label = QLabel(f"{emoji} {title}")
        title_label.setStyleSheet("font-weight: bold; font-size: 16pt; color: #00C853;")
        layout.addWidget(title_label)

        # Conteúdo
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("line-height: 1.5; color: #7A7E8F; font-size: 11pt;")
        layout.addWidget(content_label)

        layout.addStretch()
        self.setLayout(layout)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # ========== CABEÇALHO ==========
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)

        title = QLabel("🎬 VidPulse")
        title.setStyleSheet("font-size: 38pt; font-weight: bold; background: transparent;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(
            "Download de vídeos e áudio do YouTube\n"
            "com qualidade, rapidez e uma interface que você vai adorar."
        )
        subtitle.setStyleSheet("color: #7A7E8F; font-size: 14pt; background: transparent;")
        subtitle.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        # ========== CARDS EM GRADE 2x2 ==========
        grid_layout = QGridLayout()
        grid_layout.setSpacing(25)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Card 1: Funcionalidades principais
        features_card = Card(
            "🚀 Funcionalidades",
            "• Download de vídeos (MP4, WebM, MKV)\n"
            "• Download de áudio (MP3, AAC, OGG, M4A)\n"
            "• Escolha de qualidade (Auto a 2160p)\n"
            "• Barra de progresso com tempo restante\n"
            "• Cancelamento em qualquer momento",
            "🎯"
        )
        grid_layout.addWidget(features_card, 0, 0)

        # Card 2: Temas e UI
        ui_card = Card(
            "🎨 Interface Moderna",
            "• Tema Dark / Light persistente\n"
            "• Cards elegantes com sombras\n"
            "• Layout responsivo e limpo\n"
            "• Abas organizadas nas configurações",
            "✨"
        )
        grid_layout.addWidget(ui_card, 0, 1)

        # Card 3: Privacidade e Cookies
        cookies_card = Card(
            "🍪 Suporte a Cookies",
            "• Vídeos com restrição de idade\n"
            "• Conteúdo bloqueado por região\n"
            "• Carregue seu cookies.txt nas configurações",
            "🔒"
        )
        grid_layout.addWidget(cookies_card, 1, 0)

        # Card 4: Prévia e Configurações
        preview_card = Card(
            "👁️ Prévia Externa",
            "• Assista ao vídeo no seu player favorito\n"
            "• Antes de baixar, confirme o conteúdo\n"
            "• Configurações avançadas personalizáveis",
            "⚙️"
        )
        grid_layout.addWidget(preview_card, 1, 1)

        main_layout.addLayout(grid_layout)

        # ========== CARD DE VERSÃO (full width) ==========
        version_card = Card(
            "📦 Estado do Projeto",
            "Versão atual: **v1.0** – estável e pronta para uso.\n\n"
            "✔️ Download funcional\n"
            "✔️ Configurações persistentes\n"
            "✔️ Suporte a múltiplos formatos\n"
            "✔️ Cancelamento e ETA\n\n"
            "🔜 Em breve: downloads simultâneos e corte de vídeo.",
            "🧪"
        )
        main_layout.addWidget(version_card)

        main_layout.addStretch()

        # ========== FOOTER ==========
        footer = QLabel(
            "© Orbytek • Diony da Silva Costa\n"
            "Projeto educacional para alunos da SharkCoders Aveiro"
        )
        footer.setStyleSheet("font-size: 10pt; color: #7A7E8F; background: transparent;")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)