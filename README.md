# 🎬 VidPulse

**VidPulse** é uma aplicação desktop para Windows desenvolvida em Python com PySide6, que permite baixar vídeos e áudios do YouTube de forma simples, rápida e com uma interface moderna.

![VidPulse Screenshot](assets/screenshot.png) *(opcional)*

## ✨ Funcionalidades

- ⬇️ **Download de vídeos** em MP4, WebM, MKV (escolha o formato)
- 🎵 **Download de áudio** em MP3, AAC, OGG, M4A
- 🎚️ **Escolha de qualidade** (Auto, 2160p até 360p)
- 🎨 **Tema Dark / Light** (persistente)
- 🍪 **Suporte a cookies** para vídeos com restrição de idade ou região
- ⏸️ **Cancelamento de download** a qualquer momento
- ⏱️ **Barra de progresso com tempo restante (ETA)**
- 👁️ **Prévia externa** do vídeo (abre no seu player favorito)
- ⚙️ **Configurações avançadas** (pastas padrão, qualidade padrão, formatos, etc.)
- 💾 **Persistência de todas as configurações** (tema, pastas, formatos, qualidade)

## 🛠️ Tecnologias utilizadas

- Python 3.10+
- [PySide6](https://doc.qt.io/qtforpython-6/) – Interface gráfica Qt6
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) – Download de mídia do YouTube
- [FFmpeg](https://ffmpeg.org/) – Conversão e manipulação de áudio/vídeo

## 📁 Estrutura do projeto

```
VidPulse/
│
├── main.py
├── requirements.txt
│
├── core/
│ ├── downloader.py # Lógica de download e extração
│ ├── utils.py # Utilitários de caminhos
│ └── config.py # Gerenciamento de configurações (QSettings)
│
├── ui/
│ ├── main_window.py
│ ├── download_worker.py
│ │
│ ├── pages/
│ │ ├── home_page.py
│ │ ├── downloader_page.py
│ │ └── settings_page.py
│ │
│ ├── widgets/
│ │ └── theme_manager.py
│ │
│ └── styles/
│ ├── dark.qss
│ └── light.qss
│
├── assets/
│ ├── icon.png
│ └── VidPulse.png
│
├── ffmpeg/
│ ├── ffmpeg.exe
│ └── ffprobe.exe
│
└── cookies.txt (opcional)
```

## 🚀 Como executar

1. **Clone o repositório**
   ```bash
   git clone https://github.com/SEU_USER/VidPulse.git
   cd VidPulse
    ```

2. Instalar dependências:

    ```bash
    python -m venv venv
    venv\Scripts\activate   # Windows
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

3. Executar:

    ```bash
    python main.py
    ```

## ⚠️ Requisitos adicionais

* O FFmpeg já está incluído na pasta ffmpeg/ do projeto – não precisa instalar separadamente.

* Para vídeos com restrição de idade ou região, exporte os cookies do seu navegador e carregue-os nas Configurações (extensão "Get cookies.txt").

* O yt-dlp pode mostrar avisos sobre JavaScript runtime – são apenas informativos e não afetam o funcionamento.

## 📖 Guia rápido

1. Cole o link do YouTube no campo "URL".
2. Clique em Validar vídeo – verá a thumbnail, título, duração e tamanho.
3. Escolha o formato desejado (MP4 ou MP3) – os formatos reais (ex: WebM, AAC) são definidos nas Configurações.
4. Selecione a qualidade (ou mantenha "Auto").
5. Escolha a pasta de destino (ou use a padrão: Vídeos/Música).
6. Clique em Iniciar Download – acompanhe a barra de progresso e o tempo restante.
7. Ao finalizar, pode abrir a pasta do ficheiro diretamente.

## 🧪 Funcionalidades extras (roadmap)

* Prévia externa do vídeo
* Cancelamento de download
* Múltiplos formatos de saída
* Configurações persistentes
* Downloads simultâneos (fila)



## 📚 Propósito educacional

Este projeto foi desenvolvido para auxiliar alunos no aprendizado de:

* Estrutura de projetos Python profissionais
* Desenvolvimento de interfaces gráficas com Qt (PySide6)
* Integração com bibliotecas externas (yt-dlp, requests)
* Persistência de configurações com QSettings
* Boas práticas de programação (modularidade, threads, signals/slots)

**Respeite os termos de serviço do YouTube** – utilize o VidPulse apenas para conteúdos que possui permissão ou para fins educacionais.

## 👨‍💻 Autor

Diony da Silva Costa – Fundador da Orbytek
Projeto educacional para alunos da SharkCoders Aveiro

## 📄 Licença
Este projeto é distribuído sob a licença MIT. Consulte o ficheiro LICENSE para mais informações.