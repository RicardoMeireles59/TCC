# 🎬 EasyEnglish

> Aprenda idiomas de verdade — com as frases e palavras dos vídeos que você já assiste.

Sistema composto por uma **extensão para Google Chrome** e uma **aplicação web**, que trabalham juntas para transformar as legendas dos vídeos do YouTube em flashcards organizados para estudo de idiomas.

---

## 📖 Sobre o Projeto

A ideia surgiu de uma dificuldade comum: aprender inglês (ou qualquer outro idioma) com material genérico e descontextualizado. Com o EasyEnglish, o aprendizado acontece com o vocabulário e as frases dos vídeos que você já consome no dia a dia.

Enquanto você assiste, a extensão do Chrome captura as legendas em **português** e **inglês** simultaneamente. Com um clique, essas legendas são enviadas para a aplicação web, que usa inteligência artificial para identificar as palavras e frases mais relevantes e gerar flashcards prontos para estudo. Os cards ficam organizados em **baralhos**, permitindo separar o conteúdo por tema, canal, nível de dificuldade ou qualquer critério que faça sentido para você.

A revisão acontece diretamente no app web, com um sistema de repetição para garantir que o conteúdo seja fixado de forma eficiente.

---

## ✨ Funcionalidades

### Extensão Chrome
- Captura legendas em PT e EN automaticamente durante a reprodução do vídeo
- Popup com controles para iniciar/pausar a captura
- Envio das legendas para o app web com um clique
- Indicação visual do vídeo que está sendo monitorado

### App Web
- **Baralhos** — organize seus flashcards em coleções temáticas (ex: "Inglês técnico", "Gírias americanas", "Canal X")
- **Geração automática de flashcards** — IA extrai frases e vocabulário relevantes das legendas capturadas
- **Modo revisão** — vire os cards, marque como acertado ou errado e acompanhe seu progresso
- **Histórico de vídeos** — visualize quais vídeos já geraram flashcards e quando foram estudados
- **Gerenciamento de cards** — edite, exclua ou mova flashcards entre baralhos manualmente

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Backend | Python + Django |
| Frontend | HTML, CSS, JavaScript, Tailwind CSS |
| Extensão | JavaScript (Chrome Extension Manifest V3) |
| Extração de legendas | A definir (biblioteca Python) |
| IA (geração de flashcards) | A definir |
| Banco de dados | MySQL |

---

## 🗂️ Estrutura do Projeto

```
youtube-flashcards/
├── backend/                        # Django
│   ├── manage.py
│   ├── core/                       # App principal
│   │   ├── models.py               # Deck, Flashcard, CapturedCaption
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── services/
│   │       ├── caption_parser.py   # Processa legendas recebidas
│   │       └── flashcard_ai.py     # Integração com IA
│   ├── templates/
│   │   └── ...                     # HTML com Tailwind
│   ├── static/
│   │   └── ...                     # CSS e JS
│   └── requirements.txt
│
├── extension/                      # Extensão Google Chrome
│   ├── manifest.json
│   ├── content/
│   │   └── caption-capture.js      # Injeta no YouTube e captura legendas
│   ├── background/
│   │   └── service-worker.js       # Comunicação com o backend
│   └── popup/
│       ├── popup.html
│       ├── popup.css
│       └── popup.js
│
└── README.md
```

---

## 🚀 Rodando o Projeto

### Pré-requisitos

- Python 3.11+
- pip
- Google Chrome

### Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # preencha as variáveis necessárias
python manage.py migrate
python manage.py runserver
```

### Extensão Chrome

1. Abra o Chrome e acesse `chrome://extensions`
2. Ative o **Modo do desenvolvedor** no canto superior direito
3. Clique em **Carregar sem compactação**
4. Selecione a pasta `extension/`
5. Acesse qualquer vídeo no YouTube com legendas disponíveis em PT ou EN

---

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` dentro de `backend/` com base no `.env.example`:

```env
SECRET_KEY=sua_secret_key_django
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# IA para geração de flashcards
AI_API_KEY=sua_chave_aqui
```

---

## 🔄 Fluxo de Uso

1. O usuário abre um vídeo no YouTube com legendas em PT e/ou EN
2. A extensão detecta as legendas e começa a capturá-las em segundo plano
3. Ao clicar em **"Gerar Flashcards"** no popup da extensão, as legendas são enviadas para o backend
4. O backend processa o texto com IA e extrai frases e vocabulário relevantes
5. Os flashcards gerados ficam disponíveis no app web, dentro de um baralho
6. O usuário revisa os cards no modo de estudo e acompanha seu progresso

---

---

<p align="center">Feito com muito ☕ e ódio</p>
