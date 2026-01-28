"""
Modelo de dados do usuário (SQLAlchemy)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database.base import Base


class User(Base):
    """Modelo de usuário no banco de dados"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nome_completo = Column(String, nullable=False)
    senha_hash = Column(String, nullable=False)
    departamento = Column(String, nullable=True)
    cargo = Column(String, nullable=True)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    ultima_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"