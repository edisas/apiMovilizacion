from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from crud.user_crud import create_user, get_user_by_username
from database import get_db
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Verificar que solo administradores puedan registrar usuarios
    if current_user["rolId"] != 1:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")

    # Verificar si el usuario ya existe
    try:
        db_user = get_user_by_username(db, user.username)
        raise HTTPException(status_code=400, detail="Username already registered")
    except HTTPException as e:
        if e.status_code != 404:  # Solo ignorar el error si es "User not found"
            raise e

    # Crear nuevo usuario con manejo de errores
    return create_user(db, user.username, user.email, user.password, user.rolId, user.adscripcionId)
