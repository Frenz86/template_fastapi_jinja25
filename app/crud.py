from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User
from schemas import UserCreate, UserUpdate
from typing import List, Optional

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Ottiene un utente per ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Ottiene un utente per email"""
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Ottiene una lista di utenti con paginazione"""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    """Crea un nuovo utente"""
    db_user = User(
        name=user.name,
        email=user.email,
        age=user.age
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Email già esistente")

def update_user(db: Session, user_id: int, user: UserCreate) -> Optional[User]:
    """Aggiorna un utente esistente"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    try:
        db_user.name = user.name
        db_user.email = user.email
        db_user.age = user.age
        
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Email già esistente")

def delete_user(db: Session, user_id: int) -> bool:
    """Elimina un utente"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

def search_users(db: Session, query: str) -> List[User]:
    """Cerca utenti per nome o email"""
    return db.query(User).filter(
        (User.name.ilike(f"%{query}%")) | 
        (User.email.ilike(f"%{query}%"))
    ).all()