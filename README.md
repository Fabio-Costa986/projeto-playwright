# Automação de Testes — ServeRest

Projeto de automação de testes de **API** e **Frontend** para o [ServeRest](https://serverest.dev), construído com **Python + Playwright + pytest**.

---

## Tecnologias

| Ferramenta | Versão | Uso |
|---|---|---|
| Python | 3.12+ | Linguagem principal |
| Playwright | 1.51 | Automação de browser e API |
| pytest | 8.3 | Runner e organização dos testes |
| pytest-html | 4.1 | Relatório HTML |
| Faker | 37.1 | Geração de dados dinâmicos |

---

## Estrutura do Projeto

```
playwright/
├── conftest.py                  # Fixtures globais (API, browser, tracing, login)
├── pytest.ini                   # Configuração do pytest, logs e markers
├── requirements.txt
├── .env                         # Variáveis de ambiente (não versionado)
├── .env.example                 # Modelo de variáveis de ambiente
│
├── pages/                       # Page Object Model
│   ├── base_page.py             # Classe base com logger
│   ├── login_page.py
│   ├── cadastro_page.py
│   ├── home_page.py
│   ├── produto_page.py
│   └── listar_produtos_page.py
│
├── tests/
│   ├── api/                     # Testes de API REST
│   │   ├── test_login.py        # 4 testes
│   │   ├── test_usuarios.py     # 8 testes
│   │   ├── test_produtos.py     # 8 testes
│   │   └── test_carrinhos.py    # 6 testes
│   └── frontend/                # Testes de interface
│       ├── test_login.py        # 6 testes
│       ├── test_cadastro.py     # 4 testes
│       └── test_produtos.py     # 4 testes
│
├── utils/
│   └── data_factory.py          # Geração de usuários e produtos com Faker
│
└── reports/                     # Gerado automaticamente (não versionado)
    ├── report.html
    ├── tests.log
    └── traces/                  # Traces do Playwright (somente em falhas)
```

---

## Instalação

**1. Clone o repositório e acesse a pasta:**
```bash
git clone <url-do-repositorio>
cd playwright
```

**2. Crie e ative o ambiente virtual:**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Instale o browser do Playwright:**
```bash
playwright install chromium
```

**5. Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# edite o .env se necessário
```

---

## Variáveis de Ambiente

| Variável | Padrão | Descrição |
|---|---|---|
| `BASE_URL_API` | `https://serverest.dev` | URL base da API |
| `BASE_URL_FRONT` | `https://front.serverest.dev` | URL base do frontend |
| `ADMIN_EMAIL` | `fulano@qa.com` | E-mail do usuário admin |
| `ADMIN_PASSWORD` | `teste` | Senha do usuário admin |

---

## Executando os Testes

```bash
# Todos os testes
pytest

# Somente testes de API
pytest -m api

# Somente testes de Frontend
pytest -m frontend

# Modo headless (sem abrir o browser)
pytest --headed=false

# Teste específico
pytest tests/api/test_usuarios.py

# Paralelo (4 workers)
pytest -n 4
```

---

## Relatórios e Logs

Após a execução, os artefatos ficam em `reports/`:

| Arquivo | Descrição |
|---|---|
| `reports/report.html` | Relatório visual completo com status de cada teste |
| `reports/tests.log` | Log detalhado em arquivo (nível DEBUG) |
| `reports/traces/*.zip` | Trace do Playwright — gerado **somente em falhas** |

**Para abrir um trace após uma falha:**
```bash
playwright show-trace reports/traces/nome_do_teste.zip
```

O viewer exibe screenshots, DOM interativo e requisições de rede por passo.

---

## Cobertura dos Testes

### API — `https://serverest.dev`

| Módulo | Cenários cobertos |
|---|---|
| `/login` | Credenciais válidas, e-mail inválido, senha inválida, campos obrigatórios |
| `/usuarios` | Listar, criar, duplicar e-mail, buscar por ID, editar, deletar, ID inexistente |
| `/produtos` | Listar, criar (autenticado/não autenticado), duplicar nome, buscar, editar, deletar |
| `/carrinhos` | Listar, criar, segundo carrinho, concluir compra, cancelar compra, buscar por ID |

### Frontend — `https://front.serverest.dev`

| Módulo | Cenários cobertos |
|---|---|
| Login | Login válido, credenciais inválidas, campos obrigatórios, logout, link de cadastro |
| Cadastro | Usuário válido, e-mail duplicado, campos obrigatórios, perfil admin |
| Produtos | Listagem, cadastro, link de cadastro visível, campos obrigatórios |

---

## Arquitetura

### Page Object Model
Cada página do frontend é representada por uma classe em `pages/`. Isso desacopla a lógica de navegação dos testes, facilitando a manutenção quando seletores mudam.

### Fixtures
| Fixture | Escopo | Descrição |
|---|---|---|
| `api_context` | sessão | Contexto HTTP sem autenticação |
| `auth_token` | sessão | Token Bearer obtido via login |
| `auth_api_context` | sessão | Contexto HTTP com header `Authorization` |
| `page` | teste | Página do browser com tracing ativo |
| `logged_page` | teste | Página já autenticada como admin |

### Logs
- **Terminal**: nível `INFO` em tempo real durante a execução
- **Arquivo**: nível `DEBUG` em `reports/tests.log`
- Cada page object loga suas ações com o próprio nome como identificador

### Tracing on Failure
O Playwright Tracing é iniciado em todo teste de frontend e descartado se o teste passar. Em caso de falha, o arquivo `.zip` é salvo em `reports/traces/` automaticamente.
