from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from src.app.apis.utils import OAuth2PasswordBearerWithCookie
from config import settings
from src.app.security.security import create_access_token
from src.db.repository.users import get_user

from src.db.repository.users import check_hash

from jose import jwt
from jose import JWTError
from src.db.schemas.tokens import Token

# from fastapi.security import OAuth2PasswordBearer


login = APIRouter()


def authenticate_user(username: str, password: str):
    user = get_user(username)
    print(user)

    if not user:
        return False
    if not check_hash(password, user.hashed_password):
        return False
    return user


@login.post("/token", response_model=Token)
def login_for_access_token(response: Response,
                           form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearerWithCookie(token_url="/login/token")


def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        print("username/email extracted is ", username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return user