# 📚 App Histórico de Estudos - EasyEnglish

## Estrutura da App

```
back-end/historico/
├── __init__.py
├── admin.py              # Admin interface para EstudoSessao
├── apps.py              # Configuração da app
├── migrations/          # Migrações do banco de dados
│   └── __init__.py
├── models.py            # Modelo EstudoSessao
├── tests.py             # Testes da app
├── urls.py              # Rotas URL da app
├── views.py             # Views (historico_view, get_history_data)
├── templates/
│   └── historico/
│       └── index.html   # Template da página de histórico
└── static/
    └── historico/
        ├── style.css    # Estilos (Design System)
        └── script.js    # Lógica JavaScript
```

## Configuração

### 1. Adicionar à `settings.py`
A app `historico` já foi adicionada ao `INSTALLED_APPS`.

### 2. Criar as Migrações
```bash
python manage.py makemigrations historico
python manage.py migrate
```

### 3. URLs Disponíveis
- `GET /historico/` - Página de histórico de estudos
- `GET /historico/api/dados/` - API para carregar dados do histórico (JSON)

## Modelos

### EstudoSessao
Registra cada sessão de estudo do usuário.

**Campos:**
- `user` - Relacionado ao usuário (ForeignKey)
- `data` - Data e hora da sessão (auto_now_add)
- `cards_estudados` - Total de cards estudados
- `acertos` - Quantidade de acertos
- `erros` - Quantidade de erros
- `duracao_minutos` - Duração da sessão em minutos

**Propriedades:**
- `taxa_acerto` - Porcentagem de acertos calculada automaticamente

## Views

### historico_view(request)
Renderiza a página de histórico. Requer autenticação.

**URL:** `/historico/`
**Método:** GET
**Template:** `historico/index.html`

### get_history_data(request)
Retorna os dados do histórico em formato JSON.

**URL:** `/historico/api/dados/`
**Método:** GET
**Retorno:**
```json
{
  "success": true,
  "data": [
    {
      "date": "2026-06-10",
      "cardsStudied": 15,
      "correct": 12,
      "incorrect": 3,
      "duration": "12 min"
    },
    ...
  ]
}
```

## Frontend

### Funcionalidades
- 📊 Visualização de estatísticas gerais (sessões, cards, acertos, erros)
- 📅 Tabela com histórico de estudos filtrada por data
- 🔍 Busca por data
- 📈 Filtro por taxa de acerto (>70% ou <70%)
- 🎨 Modo escuro/claro com localStorage
- 📱 Design responsivo

### Estilo
O frontend segue o **Design System** do EasyEnglish:
- Tipografia: Inter 400, 500, 600, 700
- Border radius: 4px, 6px, 8px, 12px, 20px, 50%
- Paleta de cores: Dark Mode (padrão) e White Mode
- Variáveis CSS para fácil customização

## Próximos Passos

### 1. Conectar com Banco de Dados
Quando os flashcards forem criados/revisados, registrar as sessões:
```python
from historico.models import EstudoSessao

EstudoSessao.objects.create(
    user=request.user,
    cards_estudados=20,
    acertos=16,
    erros=4,
    duracao_minutos=18
)
```

### 2. API para Criar Sessões
Criar endpoint POST `/historico/api/sessoes/` para registrar novas sessões.

### 3. Gráficos
Adicionar gráficos de progresso ao longo do tempo (use: Chart.js ou Plotly.js).

## Comandos Úteis

```bash
# Gerar migration
python manage.py makemigrations historico

# Aplicar migrations
python manage.py migrate historico

# Criar superuser (se necessário)
python manage.py createsuperuser

# Rodar testes
python manage.py test historico

# Shell interativo
python manage.py shell
```

## Admin Interface

Acesse `/admin/` para gerenciar EstudoSessao através da interface Django admin.

Listagem mostra: Usuário, Data, Cards Estudados, Acertos, Erros, Taxa de Acerto
