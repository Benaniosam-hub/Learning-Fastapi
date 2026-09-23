from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from passlib.context import CryptContext


# =========================================================
# JWT Configuration
# =========================================================

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# =========================================================
# Password Hashing
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================================================
# Verify Password
# =========================================================

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =========================================================
# Create JWT Access Token
# =========================================================

def create_access_token(
    user_id: int,
    role: str
) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# =========================================================
# Get Current Authenticated User
# =========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        # Decode JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Get user ID from "sub"
        user_id = payload.get("sub")

        # Get role from JWT
        role = payload.get("role")

        # Both are required
        if user_id is None or role is None:
            raise credentials_exception

        # Convert user ID to integer
        user_id = int(user_id)

        return {
            "user_id": user_id,
            "role": role
        }

    except (JWTError, ValueError):

        raise credentials_exception


# =========================================================
# Require Admin
# =========================================================

def require_admin(
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user