# 🚀 Configuração Rápida - App Histórico

## Passo 1: Criar Migração

```bash
cd repo-easy-english
python manage.py makemigrations historico
```

Você verá:
```
Migrations for 'historico':
  historico/migrations/0001_initial.py
    - Create model EstudoSessao
```

## Passo 2: Aplicar Migração

```bash
python manage.py migrate
```

Você verá:
```
Running migrations:
  Applying historico.0001_initial... OK
```

## Passo 3: Coletar Arquivos Estáticos (Produção)

```bash
python manage.py collectstatic --noinput
```

## Passo 4: Testar a App

```bash
python manage.py runserver
```

Acesse: `http://localhost:8000/historico/`

## Verificar Admin

1. Acesse `http://localhost:8000/admin/`
2. Faça login com seu superuser
3. Você verá "Histórico de Estudos" → "Sessões de Estudo" na sidebar

## URLs Disponíveis

| URL | Método | Descrição |
|-----|--------|-----------|
| `/historico/` | GET | Página de histórico |
| `/historico/api/dados/` | GET | API JSON com dados |

## Estrutura de Pastas

```
back-end/historico/
├── migrations/           # Pasta de migrações do BD
│   ├── __init__.py
│   └── 0001_initial.py  # ← Será criada aqui
├── static/historico/
│   ├── style.css         # Estilos
│   └── script.js         # JavaScript
├── templates/historico/
│   └── index.html        # Template HTML
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── urls.py
├── views.py
└── README.md
```

## Resolução de Problemas

### Erro: "No module named 'historico'"
✓ Confirme que `'historico'` está em `INSTALLED_APPS` no settings.py

### Erro: "TemplateDoesNotExist"
✓ Confirme que a pasta `templates/historico/` existe com index.html

### Erro: "Static files not found"
✓ Execute `python manage.py collectstatic` (produção)
✓ Em desenvolvimento, o Django serve automático

## Próximos Passos

1. **Conectar ao formulário de estudos** - Registrar EstudoSessao quando usuário termina de estudar
2. **Adicionar gráficos** - Visualizar progresso ao longo do tempo
3. **Exportar dados** - Download de relatório em PDF/CSV

---

**Dúvidas?** Veja `back-end/historico/README.md` para documentação completa.
