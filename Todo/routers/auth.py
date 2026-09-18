from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_connection
from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

connection = None
cursor = None

@router.get("/auth/{id}")
async def get_user(id: int):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            '''
            select * from users where id = %s
            ''',
            (id,)
        )

        user = cursor.fetchone()

        return user

    except Exception as e:
        return{
            "error":str(e)
        }

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

        

@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):

    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = bcrypt_context.hash(create_user_request.password)

    try:
        cursor.execute( '''
            insert into users
            (
                email,
                username,
                first_name,
                last_name,
                role,
                hashed_password,
                is_active
            )
            Values
            (%s,%s,%s,%s,%s,%s,%s)
            returning *
        ''',
        (create_user_request.email,
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

        return row

    except Exception as e:
        return{
            "error": str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()




# SECRET_KEY = "my-secret-key"
# ALGORITHM = "HS256"

# bcrypt_context = CryptContext(
#     schemes = ["bcrypt"],
#     deprecated = "auto"
# )

# def verify_password(plain_password, hashed_password):
#     return bcrypt_context.verify(
#         plain_password,
#         hashed_password
#     )
