# 🎬 EasyEnglish

> Aprenda idiomas com as frases e palavras dos vídeos que você já assiste.

Sistema composto por uma **extensão para Google Chrome** e uma **aplicação web**, que trabalham juntas para transformar as legendas dos vídeos do YouTube em flashcards organizados para estudo de idiomas.

---

## 📖 Sobre o Projeto

A ideia surgiu de uma dificuldade comum: aprender inglês (ou qualquer outro idioma) com material genérico e descontextualizado. Com o EasyEnglish, o aprendizado acontece com o vocabulário e as frases dos vídeos que você já consome no dia a dia.

Enquanto você assiste, a extensão do Chrome captura as legendas em inglês. Essas legendas são tratadas e traduzidas para português, e depois são enviadas para a aplicação web, que gera flashcards prontos para estudo. Os cards ficam organizados em **baralhos**, permitindo separar o conteúdo por tema, canal, nível de dificuldade ou qualquer critério que faça sentido para você.

A revisão acontece diretamente no app web, com um sistema de repetição para garantir que o conteúdo seja fixado de forma eficiente.

---

## ✨ Funcionalidades

### Extensão Chrome
- Captura legendas em EN durante a reprodução do vídeo
- Tradução automática EN → PT (Google Translate, sem necessidade de chave)
- Popup com controles para iniciar/pausar a captura
- Envio das legendas para o app web automaticamente
- Criação manual de flashcards pelo popup, com escolha do baralho

### App Web
- **Baralhos** — organize seus flashcards em coleções temáticas (ex: "Inglês técnico", "Gírias americanas", "Canal X")
- **Geração automática de flashcards** — extração de frases relevantes das legendas capturadas, agrupadas num baralho com o nome do vídeo
- **Modo revisão** — vire os cards, marque como acertado ou errado e acompanhe seu progresso
- **Histórico de estudos** — acompanhe as sessões de estudo, acertos, erros e duração
- **Gerenciamento de cards** — edite, exclua ou mova flashcards entre baralhos manualmente

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Backend | Python + Django + Django REST Framework |
| Frontend | HTML, CSS, JavaScript (templates Django) |
| Extensão | JavaScript (Chrome Extension Manifest V3) |
| Tradução das legendas | Google Translate (endpoint público, sem chave) |
| Banco de dados | SQLite (desenvolvimento) · MySQL (previsto para produção) |

---

## 🗂️ Estrutura do Projeto

```
repo-easy-english/
├── manage.py
├── requirements.txt
├── db.sqlite3                             # Banco de desenvolvimento (SQLite)
│
├── easyenglish/                           # Projeto Django + app web
│   ├── settings.py / urls.py / wsgi.py
│   ├── web_urls.py                        # Rotas do app web (auth, dashboard, flashcards, baralhos)
│   ├── models.py                          # EstudoSessao (histórico de estudo)
│   ├── views.py                           # Auth, dashboard, CRUD de flashcards e baralhos, histórico
│   ├── forms.py                           # RegisterForm, LoginForm, FlashcardForm, DeckForm
│   ├── services/
│   │   └── dashboard_service.py           # Busca, filtros e ordenação da lista de flashcards
│   ├── templatetags/                      # Ícones SVG e cache bust
│   ├── templates/                         # auth, dashboard, decks, flashcards, historico, components
│   └── static/                            # CSS e JS do app web
│
├── extensao/                              # App Django da API + código da extensão
│   ├── models.py                          # Deck, Flashcard, CapturedSentence, Video
│   ├── views.py                           # API REST (token): captions, sentences, flashcards, decks
│   ├── urls.py                            # Rotas /extensao/api/...
│   ├── middleware.py                      # Isenção de CSRF para a API
│   ├── migrations/
│   └── chrome_extension/                  # Extensão Google Chrome (Manifest V3)
│       ├── manifest.json
│       ├── captura_legendas_automatico/
│       │   ├── page_reader.js             # Lê as legendas do player do YouTube
│       │   ├── content.js                 # Content script (coleta e repassa as legendas)
│       │   └── background.js              # Service worker: traduz EN→PT e envia ao backend
│       ├── pagina_login/                  # Login da extensão (gera token de acesso à API)
│       ├── pagina_flashcards/             # Popup: controles de captura e criação manual de cards
│       └── icons/
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
git clone https://github.com/RicardoMeireles59/TCC.git
cd TCC

python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

O app estará disponível em `http://localhost:8000`. Crie sua conta na tela de registro (`/register/`) — a mesma conta é usada para fazer login na extensão.

Comandos úteis:

```bash
python manage.py test              # roda a suíte de testes
python manage.py createsuperuser   # acesso ao admin em /admin/ (opcional)
```

### Extensão Chrome

1. Abra o Chrome e acesse `chrome://extensions`
2. Ative o **Modo do desenvolvedor** no canto superior direito
3. Clique em **Carregar sem compactação**
4. Selecione a pasta `extensao/chrome_extension/`
5. Clique no ícone da extensão e faça login com a conta criada no app web
6. Acesse qualquer vídeo no YouTube com legendas disponíveis em EN e ative a captura

> ⚠️ O backend precisa estar rodando em `http://localhost:8000` para a extensão funcionar.

---

## ⚙️ Variáveis de Ambiente

O projeto roda sem nenhuma configuração extra — todas as variáveis têm valor padrão para desenvolvimento. Para personalizar, crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_secret_key_django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 🔄 Fluxo de Uso

1. O usuário abre um vídeo no YouTube com legendas em EN
2. A extensão detecta as legendas e começa a capturá-las em segundo plano
3. As legendas são tratadas, traduzidas para PT e enviadas ao backend
4. O backend divide o texto em frases e gera flashcards, agrupados num baralho com o nome do vídeo
5. O usuário revisa os cards no modo de estudo e acompanha seu progresso no histórico

---

<p align="center">Feito com muito ☕</p>
