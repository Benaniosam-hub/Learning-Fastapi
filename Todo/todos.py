from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import get_connection
from routers.authz import get_current_user, require_admin


router = APIRouter()


# =========================================================
# Pydantic Models
# =========================================================

class Todo(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool


class TodoUpdate(BaseModel):
    title: str


# =========================================================
# Home
# =========================================================

@router.get("/")
def home():
    return {
        "message": "FastAPI is running"
    }


# =========================================================
# GET TODOS
# USER  -> Only their own todos
# ADMIN -> All todos
# =========================================================

@router.get("/todos")
async def get_todos(
    current_user: dict = Depends(get_current_user)
):
    role = current_user.get("role")

    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # -----------------------------------------
        # ADMIN: Get all todos
        # -----------------------------------------

        if current_user["role"] == "admin":

            cursor.execute(
                """
                SELECT *
                FROM todos
                ORDER BY id
                """
            )

        # -----------------------------------------
        # USER: Get only own todos
        # -----------------------------------------

        else:

            cursor.execute(
                """
                SELECT *
                FROM todos
                WHERE owner_id = %s
                ORDER BY id
                """,
                (current_user["user_id"],)
            )

        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        todos = [
            dict(zip(columns, row))
            for row in rows
        ]

        return todos

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch todos"
        )

    finally:

        cursor.close()
        connection.close()


# =========================================================
# SEARCH TODO BY TITLE
#
# USER  -> Search only own todos
# ADMIN -> Search all todos
# =========================================================

@router.get("/todos/search")
async def get_todo_by_title(
    title: str,
    current_user: dict = Depends(get_current_user)
):
    role = current_user.get("role")
    
    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:

        if current_user["role"] == "admin":

            cursor.execute(
                """
                SELECT *
                FROM todos
                WHERE title = %s
                """,
                (title,)
            )

        else:

            cursor.execute(
                """
                SELECT *
                FROM todos
                WHERE title = %s
                AND owner_id = %s
                """,
                (
                    title,
                    current_user["user_id"]
                )
            )

        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        todos = [
            dict(zip(columns, row))
            for row in rows
        ]

        return todos

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to search todos"
        )

    finally:

        cursor.close()
        connection.close()


# =========================================================
# GET TODO BY ID
#
# USER  -> Can get only their own todo
# ADMIN -> Can get any todo
# =========================================================

@router.get("/todos/{id}")
async def get_todo_by_id(
    id: int,
    current_user: dict = Depends(get_current_user)
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # -----------------------------------------
        # ADMIN: Can access any todo
        # -----------------------------------------

        if current_user["role"] == "admin":

            cursor.execute(
                """
                SELECT *
                FROM todos
                WHERE id = %s
                """,
                (id,)
            )

        # -----------------------------------------
        # USER: Can access only own todo
        # -----------------------------------------

        else:

            cursor.execute(
                """
                SELECT *
                FROM todos
                WHERE id = %s
                AND owner_id = %s
                """,
                (
                    id,
                    current_user["user_id"]
                )
            )

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Todo not found"
            )

        columns = [column[0] for column in cursor.description]

        todo = dict(zip(columns, row))

        return todo

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch todo"
        )

    finally:

        cursor.close()
        connection.close()



# =========================================================
# CREATE TODO
#
# USER  -> Can create own todo
# ADMIN -> Can create todo
#
# owner_id comes from JWT
# NOT from Postman
# =========================================================

@router.post("/todos/create_todos")
async def create_todos(
    todo: Todo,
    current_user: dict = Depends(get_current_user)
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO todos
            (
                title,
                description,
                priority,
                complete,
                owner_id
            )
            VALUES
            (%s, %s, %s, %s, %s)
            RETURNING *
            """,
            (
                todo.title,
                todo.description,
                todo.priority,
                todo.complete,

                # IMPORTANT:
                # owner_id comes from JWT
                current_user["user_id"]
            )
        )

        row = cursor.fetchone()

        connection.commit()

        columns = [column[0] for column in cursor.description]

        created_todo = dict(zip(columns, row))

        return {
            "message": "Todo created successfully",
            "todo": created_todo
        }

    except Exception:
        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to create todo"
        )

    finally:

        cursor.close()
        connection.close()


# =========================================================
# UPDATE TODO
#
# ADMIN ONLY
# =========================================================

@router.put("/todos/{id}")
async def update_todos_title_by_id(
    id: int,
    todo: TodoUpdate,
    current_user: dict = Depends(require_admin)
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE todos
            SET title = %s
            WHERE id = %s
            RETURNING *
            """,
            (
                todo.title,
                id
            )
        )

        row = cursor.fetchone()

        if row is None:

            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="Todo not found"
            )

        connection.commit()

        columns = [column[0] for column in cursor.description]

        updated_todo = dict(zip(columns, row))

        return {
            "message": "Todo updated successfully",
            "todo": updated_todo,
            "updated_by": current_user["user_id"],
            "role": current_user["role"]
        }

    except HTTPException:
        raise

    except Exception:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to update todo"
        )

    finally:

        cursor.close()
        connection.close()


# =========================================================
# DELETE TODO
#
# ADMIN ONLY
# =========================================================

@router.delete("/todos/{id}")
async def delete_todos_by_id(
    id: int,
    current_user: dict = Depends(require_admin)
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM todos
            WHERE id = %s
            RETURNING id
            """,
            (id,)
        )

        deleted_todo = cursor.fetchone()

        if deleted_todo is None:

            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="Todo not found"
            )

        connection.commit()

        return {
            "message": "Todo deleted successfully",
            "todo_id": deleted_todo[0],
            "deleted_by": current_user["user_id"],
            "role": current_user["role"]
        }

    except HTTPException:
        raise

    except Exception:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to delete todo"
        )

    finally:

        cursor.close()
        connection.close()