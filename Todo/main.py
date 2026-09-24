from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import get_connection
from routers import auth
from todos import router as todos_router
from routers.authz import verify_password, create_access_token


app = FastAPI()


# Register routers
app.include_router(auth.router)
app.include_router(todos_router)


# -------------------------
# Login Request Model
# -------------------------

class LoginRequest(BaseModel):
    username: str
    password: str


# -------------------------
# Login
# -------------------------

@app.post("/login")
async def login_with_username_pwd(data: LoginRequest):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Get user from database
        cursor.execute(
            """
            SELECT id, username, hashed_password, is_active, role
            FROM users
            WHERE username = %s
            """,
            (data.username,)
        )

        user = cursor.fetchone()

        # User does not exist
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        # Extract user information
        user_id = user[0]
        username = user[1]
        hashed_password = user[2]
        is_active = user[3]
        role = user[4]

        # Check password
        if not verify_password(
            data.password,
            hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        # Check account status
        if not is_active:
            raise HTTPException(
                status_code=403,
                detail="User account is inactive"
            )


        # Create JWT token
        token = create_access_token(
            user_id=user_id,
            role=role
        )


        return {
            "access_token": token,
            "token_type": "bearer"
        }

    finally:
        cursor.close()
        connection.close()