"""
Schemas Pydantic para validação de dados
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class UserBase(BaseModel):
    """Schema base do usuário"""
    email: EmailStr
    nome_completo: str = Field(..., min_length=3, max_length=100)
    departamento: Optional[str] = None
    cargo: Optional[str] = None
    ativo: bool = True


class UserCreate(UserBase):
    """Schema para criação de usuário"""
    senha: str = Field(..., min_length=8)
    
    @field_validator('senha')
    @classmethod
    def senha_forte(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Senha deve conter ao menos uma letra maiúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('Senha deve conter ao menos uma letra minúscula')
        if not re.search(r'\d', v):
            raise ValueError('Senha deve conter ao menos um número')
        return v


class UserUpdate(BaseModel):
    """Schema para atualização de usuário"""
    nome_completo: Optional[str] = Field(None, min_length=3, max_length=100)
    departamento: Optional[str] = None
    cargo: Optional[str] = None
    ativo: Optional[bool] = None


class UserResponse(UserBase):
    """Schema de resposta do usuário"""
    id: int
    data_criacao: datetime
    ultima_atualizacao: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema do token JWT"""
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    """Schema para login"""
    email: EmailStr
    senha: str