# 🚀 API de Gestão de Usuários - FastAPI

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Sistema corporativo completo para gerenciamento de usuários com autenticação JWT, validação de dados robusta e arquitetura em camadas profissional.

## 📋 Sobre o Projeto

API RESTful desenvolvida com **FastAPI** seguindo as melhores práticas de desenvolvimento, incluindo:

- ✅ **Autenticação JWT** - Tokens seguros com expiração
- ✅ **Criptografia de senhas** - Bcrypt para máxima segurança
- ✅ **Validação inteligente** - Senhas fortes obrigatórias
- ✅ **Arquitetura em camadas** - Repository Pattern + Service Layer
- ✅ **CRUD completo** - Create, Read, Update, Delete
- ✅ **Soft Delete** - Desativação sem perda de dados
- ✅ **Documentação automática** - Swagger UI integrado
- ✅ **Filtros avançados** - Por departamento, status, etc.

## 🎯 Funcionalidades

### Autenticação
- Cadastro de novos usuários
- Login com geração de token JWT
- Validação de senhas fortes (maiúsculas, minúsculas, números)
- Tokens com expiração configurável (30 minutos padrão)

### Gestão de Usuários
- Listar todos os usuários (com filtros)
- Buscar usuário por ID
- Ver perfil do usuário autenticado
- Atualizar dados do usuário
- Desativar usuário (soft delete)

### Segurança
- Senhas nunca armazenadas em texto puro
- Hash com Bcrypt (salt automático)
- Proteção contra SQL Injection (ORM)
- Validação de dados em múltiplas camadas
- CORS configurado

## 🛠️ Tecnologias

| Tecnologia | Descrição |
|------------|-----------|
| **Python 3.10+** | Linguagem principal |
| **FastAPI** | Framework web moderno e rápido |
| **SQLAlchemy** | ORM para banco de dados |
| **Pydantic** | Validação de dados |
| **JWT** (Python-JOSE) | Autenticação stateless |
| **Bcrypt** (Passlib) | Criptografia de senhas |
| **SQLite** | Banco de dados (dev) |
| **Uvicorn** | Servidor ASGI de alta performance |

## 📁 Arquitetura do Projeto
```
user-management-api/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Configurações (carrega .env)
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py                # Base do SQLAlchemy
│   │   └── connection.py          # Engine e Sessions
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py                # Modelo ORM (tabela users)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py                # Schemas Pydantic (validação)
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user_repository.py     # Camada de acesso ao banco
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py        # Lógica de negócio
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── user_routes.py         # Endpoints da API
│   │
│   ├── __init__.py
│   └── main.py                    # Aplicação principal
│
├── tests/
│   ├── __init__.py
│   └── test_users.py              # Testes automatizados
│
├── .env.example                   # Exemplo de variáveis de ambiente
├── .gitignore                     # Arquivos ignorados pelo Git
├── requirements.txt               # Dependências do projeto
└── README.md                      # Este arquivo
```

### 🏗️ Padrão de Camadas
```
Cliente → Routes → Services → Repositories → Database
            ↓         ↓            ↓
         Schemas   Lógica      Queries SQL
```

**Vantagens:**
- ✅ Separação clara de responsabilidades
- ✅ Fácil manutenção e testes
- ✅ Reutilização de código
- ✅ Escalabilidade

## ⚙️ Instalação e Configuração

### Pré-requisitos

- Python 3.10 ou superior
- Git

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/EngSamir/user-management-api.git
cd user-management-api
```

### 2️⃣ Crie e ative o ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure as variáveis de ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env e ALTERE os valores (especialmente SECRET_KEY!)
```

**⚠️ IMPORTANTE:** Gere uma SECRET_KEY segura:

**Windows (PowerShell):**
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

**Linux/Mac:**
```bash
openssl rand -hex 32
```

Cole o resultado no `.env`:
```env
SECRET_KEY=sua_chave_gerada_aqui
```

### 5️⃣ Execute a aplicação
```bash
uvicorn app.main:app --reload
```

A API estará disponível em: **http://localhost:8000**

## 📚 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI (Interativo):** http://localhost:8000/docs
- **ReDoc (Documentação):** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## 🔐 Endpoints

### 🌐 Públicos (Não requerem autenticação)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações da API |
| GET | `/health` | Status de saúde |
| POST | `/auth/registro` | Cadastrar novo usuário |
| POST | `/auth/login` | Login (retorna JWT) |

### 🔒 Protegidos (Requerem token JWT)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/users/me` | Perfil do usuário autenticado |
| GET | `/users/` | Listar usuários (com filtros) |
| GET | `/users/{id}` | Buscar usuário por ID |
| PUT | `/users/{id}` | Atualizar dados do usuário |
| DELETE | `/users/{id}` | Desativar usuário |

## 🧪 Exemplos de Uso

### 1. Cadastrar Usuário
```bash
POST /auth/registro
Content-Type: application/json

{
  "email": "joao.silva@empresa.com",
  "nome_completo": "João Silva",
  "senha": "SenhaForte123",
  "departamento": "TI",
  "cargo": "Desenvolvedor",
  "ativo": true
}
```

**Resposta (201 Created):**
```json
{
  "id": 1,
  "email": "joao.silva@empresa.com",
  "nome_completo": "João Silva",
  "departamento": "TI",
  "cargo": "Desenvolvedor",
  "ativo": true,
  "data_criacao": "2026-01-28T03:00:00",
  "ultima_atualizacao": "2026-01-28T03:00:00"
}
```

### 2. Fazer Login
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "joao.silva@empresa.com",
  "senha": "SenhaForte123"
}
```

**Resposta (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Acessar Rota Protegida
```bash
GET /users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4. Listar Usuários com Filtro
```bash
GET /users/?departamento=TI&ativo=true
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🔒 Regras de Validação

### Senha Forte
- ✅ Mínimo 8 caracteres
- ✅ Pelo menos 1 letra maiúscula
- ✅ Pelo menos 1 letra minúscula
- ✅ Pelo menos 1 número

### Email
- ✅ Formato válido (validação Pydantic)
- ✅ Único no sistema

### Nome Completo
- ✅ Mínimo 3 caracteres
- ✅ Máximo 100 caracteres

## 🧪 Testes
```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=app tests/

# Modo verbose
pytest -v
```

## 🚀 Deploy

### Preparação para Produção

**1. Mude o banco para PostgreSQL:**
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

**2. Use variáveis de ambiente seguras:**
```bash
export SECRET_KEY=$(openssl rand -hex 32)
export DATABASE_URL=postgresql://...
```

**3. Desabilite reload em produção:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Opções de Deploy

| Plataforma | Dificuldade | Custo |
|------------|-------------|-------|
| **Railway** | ⭐ Fácil | Grátis (tier inicial) |
| **Render** | ⭐ Fácil | Grátis (tier inicial) |
| **Heroku** | ⭐⭐ Médio | Pago |
| **AWS EC2** | ⭐⭐⭐ Avançado | Variável |
| **Docker** | ⭐⭐ Médio | Depende |

## 📦 Dependências
```
fastapi==0.109.0           # Framework web
uvicorn[standard]==0.27.0  # Servidor ASGI
sqlalchemy==2.0.25         # ORM
pydantic==2.5.3            # Validação de dados
pydantic-settings==2.1.0   # Configurações
python-jose==3.3.0         # JWT
passlib[bcrypt]==1.7.4     # Criptografia de senhas
python-multipart==0.0.6    # Upload de arquivos
pytest==7.4.3              # Testes
email-validator==2.1.0     # Validação de email
```

## 📝 Melhorias Futuras

- [ ] Implementar refresh tokens
- [ ] Sistema de roles/permissões (Admin, User, Manager)
- [ ] Reset de senha por email
- [ ] Upload de foto de perfil
- [ ] Paginação avançada
- [ ] Logs de auditoria (quem fez o quê)
- [ ] Rate limiting (proteção contra abuso)
- [ ] Testes de integração completos
- [ ] CI/CD com GitHub Actions
- [ ] Containerização com Docker
- [ ] Documentação em OpenAPI 3.1
- [ ] Migração para PostgreSQL

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Padrões de Código

- Use **type hints** em todas as funções
- Docstrings em formato Google Style
- Máximo 88 caracteres por linha (Black formatter)
- Imports organizados (isort)

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Samir Roglésio Bezerra do Rosário**

- 🌐 GitHub: [@EngSamir](https://github.com/EngSamir)
- 💼 LinkedIn: [Adicione seu LinkedIn aqui]
- 📧 Email: samiroglesio@gmail.com

## 🙏 Agradecimentos

- FastAPI pela excelente documentação
- Comunidade Python pelo suporte
- SQLAlchemy pela robustez do ORM

## 📞 Suporte

Encontrou um bug? Tem uma sugestão? 

- 🐛 Abra uma [issue](https://github.com/EngSamir/user-management-api/issues)
- 💬 Inicie uma [discussão](https://github.com/EngSamir/user-management-api/discussions)

---

<div align="center">

⭐ **Se este projeto te ajudou, deixe uma estrela!** ⭐


</div>