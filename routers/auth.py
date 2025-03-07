from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.security import create_access_token, verify_password
from crud.user_crud import get_user_by_username
from database import get_db
from schemas.user import TokenResponse
from core.dependencies import get_current_user


router = APIRouter()


@router.get("/validate-token", status_code=status.HTTP_200_OK)
def validate_token(current_user=Depends(get_current_user)):
    """
    Verifica si el token de acceso sigue siendo válido.
    Si es válido, retorna el usuario autenticado.
    """
    return {
        "message": "Token is valid",
        "user": {
            "username": current_user["username"],
            "rolId": current_user["rolId"]
        }
    }


@router.post("/token", response_model=TokenResponse)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username, "rolId": user.rolId})
    return {"access_token": access_token, "token_type": "bearer"}

