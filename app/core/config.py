"""
Configurações centralizadas da aplicação
"""

from pydantic_settings import BaseSettings
from typing import Optional



class settings(BaseSettings):
    """Configurações da aplicação carregadas do .env"""

    # Database
    DATABASE_URL:  str


    # Segurity
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


    # API Info
    API_TITLE: str = "API de Gestão de Usuários"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Sistema corporativo para gerenciamento de usuários"


    class Config:
        env_file = ".env"
        case_sensitive = True




# Instância global das configurações
settings = settings()