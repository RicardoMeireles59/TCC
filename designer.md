EasyEnglish - Design System & Guia de Estilos


## 🔤 1. Tipografia (Fonts)

Nossa tipografia utiliza uma excelente pilha de fontes sem serifa, focada na máxima legibilidade para o aprendizado.

| Variável CSS | Valor | Uso no Projeto |
| :--- | :--- | :--- |
| `--font-family` | `'Inter', '-apple-system', sans-serif` | Fonte global de toda a aplicação. |
| `--font-size-xs` | `0.7rem` | Textos minúsculos (ex: rótulos de checkbox, info de vídeo). |
| `--font-size-sm` | `0.75rem` | Labels de formulário, links menores, textos de apoio. |
| `--font-size-md` | `0.85rem` | Tamanho base (inputs, botões, parágrafos padrões). |
| `--font-size-lg` | `1.15rem` | Subtítulos (ex: `h2` da tela de login). |
| `--font-size-xl` | `1.2rem` | Títulos de seções (ex: `h2` do dashboard) e Logo text. |
| `--font-size-2xl`| `1.5rem` | Números de destaque nos Cards de Estatísticas. |
| `--font-size-3xl`| `1.6rem` | Título principal (ex: `h1` da tela de login). |
| `--font-weight-regular` | `400` | Peso padrão do texto de leitura. |
| `--font-weight-medium` | `500` | Títulos menores, labels, notificações. |
| `--font-weight-semibold`| `600` | Botões e textos da Logo. |
| `--font-weight-bold` | `700` | Títulos de grande destaque (`h1`). |

---

## 🔲 2. Bordas e Arredondamentos (Border Radius)

O design adota cantos levemente arredondados para transmitir um visual moderno, suave e amigável.

| Variável CSS | Valor | Uso no Projeto |
| :--- | :--- | :--- |
| `--radius-sm` | `4px` | Ícones pequenos (ex: play icon). |
| `--radius-md` | `6px` | Inputs, botões principais, links da sidebar. |
| `--radius-lg` | `8px` | Cards de estatísticas, banners, vídeos recentes, toast. |
| `--radius-xl` | `12px` | Logo principal grande. |
| `--radius-pill`| `20px` | Botões outline e tags de navegação superior. |
| `--radius-full`| `50%` | Elementos perfeitamente redondos (ícone de perfil). |

---

## ☀️ 3. Sistema de Temas (Dark & White Mode)

A aplicação possui suporte a dois temas. A lógica foi construída invertendo as prioridades luminosas:
* **Dark Mode (Padrão):** Fundos escuros (`#131313`) com superfícies ligeiramente mais claras para criar profundidade.
* **White Mode (Alternativo):** Fundo base em cinza super claro (`#F4F6F8`) para não cansar a vista, superfícies brancas (`#FFFFFF`) e textos em tons de chumbo/grafite para contraste ideal.

### 🎨 Tabela de Variáveis de Cores

| Variável | Dark Mode (Atual) | White Mode (Novo) | Aplicação Principal |
| :--- | :--- | :--- | :--- |
| `--bg-base` | `#131313` | `#F4F6F8` | Fundo da tela inteira e dashboard. |
| `--bg-surface` | `#1a1a1a` | `#FFFFFF` | Cards, painel lateral (sidebar), formulários. |
| `--bg-surface-hover` | `#242424` | `#E2E8F0` | Hover de botões, inputs, ícones secundários. |
| `--border-light` | `#262626` | `#E2E8F0` | Divisões de vídeos, bordas de inputs. |
| `--border-medium` | `#333333` | `#CBD5E1` | Banners tracejados, botões outline. |
| `--text-primary` | `#ffffff` | `#0F172A` | Títulos (`h1`, `h2`), logo, números de destaque. |
| `--text-secondary` | `#e0e0e0` | `#334155` | Textos descritivos e parágrafos principais. |
| `--text-muted` | `#777777` | `#64748B` | Placeholders, labels, subtítulos, links inativos. |
| `--text-inverted` | `#000000` | `#FFFFFF` | Texto interno de botões com fundo de alto contraste. |
| `--action-primary` | `#ffffff` | `#0F172A` | Fundo do botão principal (Entrar/Cadastrar). |
| `--action-primary-hover`| `#dddddd` | `#334155` | Efeito ao passar o mouse no botão principal. |

---