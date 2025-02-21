import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, UTC
import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_jwt_token(user_name: str):
    expiration = datetime.now(UTC) + timedelta(seconds=config.token_timedelta_sec_val)
    payload = {
        "sub": user_name,
        "exp": expiration
    }
    token = jwt.encode(payload, config.sectetKey, algorithm="HS256")
    return token

def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен отсутствует"
        )
    try:
        payload = jwt.decode(token, config.sectetKey, algorithms=["HS256"])
        username: str = payload.get("sub")
        exp: int = payload.get("exp")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Не удалось проверить учетные данные"
            )

        # Проверка срока действия токена
        if datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Срок действия токена истёк"
            )

        return {"valid": True, "username": username}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Срок действия токена истёк"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось проверить учетные данные"
        )
