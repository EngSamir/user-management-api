"""
Rotas da API de usuários
"""
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
from jose import jwt, JWTError

from app.database.connection import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse, LoginRequest, Token
from app.core.config import settings

router = APIRouter(prefix="/users", tags=["Usuários"])
auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])
security = HTTPBearer()


def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verifica e valida o token JWT"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais"
        )


# Rotas de Autenticação
@auth_router.post("/registro", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário no sistema"""
    service = UserService(db)
    return service.criar_usuario(user)


@auth_router.post("/login", response_model=Token)
def login(credenciais: LoginRequest, db: Session = Depends(get_db)):
    """Realiza login e retorna token JWT"""
    service = UserService(db)
    return service.autenticar(credenciais)


# Rotas de Usuários (protegidas)
@router.get("/me", response_model=UserResponse)
def obter_usuario_atual(email: str = Depends(verificar_token), db: Session = Depends(get_db)):
    """Retorna informações do usuário autenticado"""
    from app.repositories.user_repository import UserRepository
    repo = UserRepository(db)
    user = repo.get_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return UserResponse.model_validate(user)


@router.get("/", response_model=List[UserResponse])
def listar_usuarios(
    departamento: Optional[str] = None,
    ativo: Optional[bool] = None,
    email: str = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    """Lista todos os usuários com filtros opcionais"""
    service = UserService(db)
    return service.listar_usuarios(departamento=departamento, ativo=ativo)


@router.get("/{user_id}", response_model=UserResponse)
def obter_usuario(
    user_id: int,
    email: str = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    """Obtém informações de um usuário específico"""
    service = UserService(db)
    return service.obter_usuario(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def atualizar_usuario(
    user_id: int,
    user_update: UserUpdate,
    email: str = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    """Atualiza informações de um usuário"""
    service = UserService(db)
    return service.atualizar_usuario(user_id, user_update)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def deletar_usuario(
    user_id: int,
    email: str = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    """Desativa um usuário (soft delete)"""
    service = UserService(db)
    return service.deletar_usuario(user_id)