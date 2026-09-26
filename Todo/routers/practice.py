from routers import auth
from database import get_connection
from fastapi import FastAPI, HTTPException

app = FastAPI()

app.include_router(auth.router)

connection = None
cursor = None

@app.get("/todos")
async def get_all_todos():
    connection= get_connection()
    cursor= connection.cursor()

    try:
        cursor.execute(
            'select * from todos'
        )

    except Exception:

        raise HTTPException(status_code=401,detail="Connection faild")

    finally:
        
        if cursor:
            cursor.close()

        if connection:
            cursor.close()