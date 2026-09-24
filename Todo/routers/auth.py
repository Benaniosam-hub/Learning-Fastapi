from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import get_connection
from passlib.context import CryptContext

from routers.authz import require_admin


router = APIRouter()

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================================================
# Request Models
# =========================================================

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class UpdatePasswordRequest(BaseModel):
    password: str


# =========================================================
# GET ALL USERS
# ADMIN ONLY
# =========================================================

@router.get("/auth")
async def get_all_users(current_user: dict = Depends(require_admin)):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                username,
                email,
                first_name,
                last_name,
                role,
                is_active
            FROM users
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

        columns = [
            column[0]
            for column in cursor.description
        ]

        users = [
            dict(zip(columns, row))
            for row in rows
        ]

        return users

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Failed to fetch users"
        )

    finally:

        cursor.close()
        connection.close()


# =========================================================
# GET USER BY ID
# ADMIN ONLY
# =========================================================

@router.get("/auth/{id}")
async def get_user(
    id: int,
    current_user: dict = Depends(require_admin)
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                username,
                email,
                first_name,
                last_name,
                role,
                is_active
            FROM users
            WHERE id = %s
            """,
            (id,)
        )

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        columns = [
            column[0]
            for column in cursor.description
        ]

        user = dict(zip(columns, row))

        return user

    except HTTPException:
        raise

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Failed to fetch user"
        )

    finally:

        cursor.close()
        connection.close()


# =========================================================
# CREATE USER
# ADMIN ONLY
# =========================================================

@router.post("/auth")
async def create_user(
    create_user_request: CreateUserRequest,
    current_user: dict = Depends(require_admin)
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Hash password
        hashed_password = bcrypt_context.hash(
            create_user_request.password
        )

        cursor.execute(
            """
            INSERT INTO users
            (
                email,
                username,
                first_name,
                last_name,
                role,
                hashed_password,
                is_active
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            RETURNING
                id,
                username,
                email,
                first_name,
                last_name,
                role,
                is_active
            """,
            (
                create_user_request.email,
                create_user_request.username,
                create_user_request.first_name,
                create_user_request.last_name,
                create_user_request.role,
                hashed_password,
                True
            )
        )

        row = cursor.fetchone()

        connection.commit()

        columns = [
            column[0]
            for column in cursor.description
        ]

        user = dict(zip(columns, row))

        return {
            "message": "User created successfully",
            "user": user
        }

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:

        cursor.close()
        connection.close()


# =========================================================
# UPDATE USER PASSWORD
# ADMIN ONLY
# =========================================================

@router.put("/auth/{id}")
async def update_password_by_id(
    id: int,
    update_request: UpdatePasswordRequest,
    current_user: dict = Depends(require_admin)
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Hash new password
        hashed_password = bcrypt_context.hash(
            update_request.password
        )

        cursor.execute(
            """
            UPDATE users
            SET hashed_password = %s
            WHERE id = %s
            RETURNING
                id,
                username,
                email,
                role,
                is_active
            """,
            (
                hashed_password,
                id
            )
        )

        user = cursor.fetchone()

        if user is None:

            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        connection.commit()

        columns = [
            column[0]
            for column in cursor.description
        ]

        updated_user = dict(zip(columns, user))

        return {
            "message": "Password updated successfully",
            "user": updated_user
        }

    except HTTPException:
        raise

    except Exception:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to update password"
        )

    finally:

        cursor.close()
        connection.close()


# =========================================================
# DELETE USER
# ADMIN ONLY
# =========================================================

@router.delete("/auth/{id}")
async def delete_user_by_id(
    id: int,
    current_user: dict = Depends(require_admin)
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM users
            WHERE id = %s
            RETURNING id
            """,
            (id,)
        )

        deleted_user = cursor.fetchone()

        if deleted_user is None:

            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        connection.commit()

        return {
            "message": "User deleted successfully",
            "user_id": deleted_user[0],
            "deleted_by": current_user["user_id"]
        }

    except HTTPException:
        raise

    except Exception:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to delete user"
        )

    finally:

        cursor.close()
        connection.close()