"""
Aplicação principal FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.database.connection import engine
from app.database.base import Base
from app.routes.user_routes import router as user_router, auth_router

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/", tags=["Root"])
def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "API de Gestão de Usuários",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }


@app.get("/health", tags=["Sistema"])
def health_check():
    """Verifica saúde da API"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }