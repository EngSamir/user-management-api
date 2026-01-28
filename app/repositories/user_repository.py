"""
Repositório para operações de banco de dados de usuários
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    """Repositório com operações CRUD de usuários"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuário por ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Lista todos os usuários"""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_by_departamento(self, departamento: str) -> List[User]:
        """Lista usuários por departamento"""
        return self.db.query(User).filter(User.departamento == departamento).all()
    
    def get_ativos(self) -> List[User]:
        """Lista apenas usuários ativos"""
        return self.db.query(User).filter(User.ativo == True).all()
    
    def create(self, user_data: UserCreate) -> User:
        """Cria novo usuário"""
        senha_hash = pwd_context.hash(user_data.senha)
        
        db_user = User(
            email=user_data.email,
            nome_completo=user_data.nome_completo,
            senha_hash=senha_hash,
            departamento=user_data.departamento,
            cargo=user_data.cargo,
            ativo=user_data.ativo
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Atualiza usuário existente"""
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db_user.ultima_atualizacao = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int) -> bool:
        """Soft delete - desativa usuário"""
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        
        db_user.ativo = False
        db_user.ultima_atualizacao = datetime.utcnow()
        self.db.commit()
        return True
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica se a senha está correta"""
        return pwd_context.verify(plain_password, hashed_password)