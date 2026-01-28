"""
Serviço com lógica de negócio de usuários
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from jose import jwt
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse, LoginRequest, Token
from app.models.user import User
from app.core.config import settings
from fastapi import HTTPException, status


class UserService:
    """Serviço com regras de negócio de usuários"""
    
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def criar_usuario(self, user_data: UserCreate) -> UserResponse:
        """Cria novo usuário com validações"""
        # Verifica se email já existe
        if self.repository.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        user = self.repository.create(user_data)
        return UserResponse.model_validate(user)
    
    def listar_usuarios(self, departamento: Optional[str] = None, 
                       ativo: Optional[bool] = None) -> List[UserResponse]:
        """Lista usuários com filtros opcionais"""
        if departamento:
            users = self.repository.get_by_departamento(departamento)
        elif ativo is not None:
            users = self.repository.get_ativos() if ativo else self.repository.get_all()
        else:
            users = self.repository.get_all()
        
        if ativo is not None and not departamento:
            users = [u for u in users if u.ativo == ativo]
        
        return [UserResponse.model_validate(user) for user in users]
    
    def obter_usuario(self, user_id: int) -> UserResponse:
        """Obtém usuário por ID"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return UserResponse.model_validate(user)
    
    def atualizar_usuario(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """Atualiza dados do usuário"""
        user = self.repository.update(user_id, user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return UserResponse.model_validate(user)
    
    def deletar_usuario(self, user_id: int) -> dict:
        """Desativa usuário (soft delete)"""
        if not self.repository.delete(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return {"message": "Usuário desativado com sucesso"}
    
    def autenticar(self, login_data: LoginRequest) -> Token:
        """Autentica usuário e gera token JWT"""
        user = self.repository.get_by_email(login_data.email)
        
        if not user or not self.repository.verify_password(login_data.senha, user.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        if not user.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo"
            )
        
        # Gera token JWT
        access_token = self._criar_token({"sub": user.email})
        return Token(access_token=access_token, token_type="bearer")
    
    def _criar_token(self, data: dict) -> str:
        """Cria token JWT"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)