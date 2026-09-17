# from fastapi import FastAPI
# from pydantic import BaseModel
# from database import get_connection
# from routers import auth

# app = FastAPI()
# app.include_router(auth.router)

# connection = None
# cursor = None


# class Todo(BaseModel):
#     title: str
#     description: str
#     priority: int
#     complete: bool
#     owner_id: int

# class TodoUpdate(BaseModel):
#     title: str

# @app.get("/")
# def home():
#     return {
#         "message": "FastAPI is running"
#     }


# @app.get("/todos") #Get all values
# async def get_todos():

#     connection = get_connection()
#     cursor = connection.cursor()

#     try:

#         cursor.execute("SELECT * FROM todos")

#         todo = cursor.fetchall()
#         return todo

#     except Exception as e:

#         return {
#             "error": str(e)
#         }

#     finally:
#         cursor.close()
#         connection.close()

    

# @app.get("/todos/{id}") #PATH PARAMETER
# async def get_todos_by_id(id: int):

#     connection = get_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute("SELECT * FROM todos WHERE id = %s",(id,))

#         row = cursor.fetchone()

#         if row is None:
#             return {
#                 "message": "todos not found"
#             }

#         columns = [column[0] for column in cursor.description]

#         todo = dict(zip(columns, row))

#         return todo

#     except Exception as e:
#         return {
#             "error": str(e)
#         }

#     finally:
#         cursor.close()
#         connection.close()

# @app.get("/todos/") # Query Parameter
# async def get_todos_by_title(title: str):

#     connection = get_connection()
#     cursor = connection.cursor()

#     try:  
#         cursor.execute(
#             "select * from todos where title = %s",
#             (title,) # doubt 
#         )

#         row = cursor.fetchone()

#         if row is None:
#             return {
#                 "message": "todos not found"
#             }

#         columns = [column[0] for column in cursor.description]
        
#         todo = dict(zip(columns, row))
        
#         return todo
        
#     except Exception as e:
#         return {
#             "error": str(e)
#             }
        
#     finally:
#         cursor.close()
#         connection.close()



# @app.post("/todos/create_todos")
# async def create_todos(todo: Todo):

#     connection = get_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute(
#             '''
#             insert into todos
#             (title,description,priority,complete,owner_id)
#             values
#             (%s,%s,%s,%s,%s)
#             ''',
#             (
#                 todo.title,
#                 todo.description,
#                 todo.priority,
#                 todo.complete,
#                 todo.owner_id

#             )
#         )

#         connection.commit()

#         return {
#             "message": "Todo created successfully"
#         }
    
#     except Exception as e:

#         return {
#             "error": str(e)
#         }

#     finally:

#         if cursor:
#             cursor.close()

#         if connection:
#             connection.close()



# @app.put("/todos/{id}")
# async def update_todos_title_by_id(id: int, todo: TodoUpdate):

#     connection = get_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute(
#             '''
#             update todos set title = %s where id = %s
#             ''',
#             (todo.title,id)
#         )

#         connection.commit()

#         return {
#             "message": "Successfully updated!"
#         }

#     except Exception as e:
#         return { 
#             "error": str(e)
#         }

#     finally:

#         if cursor:
#             cursor.close()

#         if connection:
#             connection.close()



# @app.delete("/todos/{id}")
# async def delete_todos_by_id(id: int):

#     connection = get_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute(
#             '''
#             delete from todos where id = %s
#             ''',
#             (id,)

#         )

#         connection.commit()

#         return {
#             "message": "Todos deleted successfully"
#         }

#     except Exception as e:
#         return{
#             "error": str(e)
#         }

#     finally:

#         if cursor:
#             cursor.close()

#         if connection:
#             connection.close()




















from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection

app = FastAPI()

connection = None
cursor = None


class Todo(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool
    owner_id: int

class UpdateTodo(BaseModel):
    title: str

#CHECKING CONNECTION:
@app.get("/")
def home():
    return {
        "Connected successfully"
    }


#GET ALL TODOS
@app.get("/todos")
async def get_todos():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute('select * from todos;')

        row = cursor.fetchall()

        return row
    
    except Exception as e:
        return {
            "error": str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            cursor.close()


#GET TODOS BY QUERY PARAMETER
@app.get("/todos/")
async def get_todos_by_query(title: str):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            'select * from todos where title =%s',
            (title,)
            )
        row = cursor.fetchone()

        column =[column[0] for column in cursor.description]

        todo = dict(zip(column,row))

        return todo

    except Exception as e:
        return{
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()

        if connection:
            cursor.close()


#GET TODOS BY PATH PARAMETER
@app.get("/todos/{id}")
async def get_todos_by_id(id:int):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            'select * from todos where id =%s',
            (id,)
        )

        row = cursor.fetchone()

        column = [column[0] for column in cursor.description]

        todo = dict(zip(column,row))

        return todo

    except Exception as e:
        return{
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


#POST CREATE NEW TODOS
@app.post("/todos/create_todo")
async def create_todos(todo: Todo):

    connection= get_connection()
    cursor=connection.cursor()

    try:

        cursor.execute(
            '''
            insert into todos
            (title,description,priority,complete,owner_id)
            values(%s,%s,%s,%s,%s)
            ''',
            (todo.title,
             todo.description,
             todo.priority,
             todo.complete,
             todo.owner_id)
        )

        connection.commit()

        return{
            "message":"todos created successfully"
        }

    except Exception as e:
        return{
            "error":str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


#UPDATE EXISTING TODOS
@app.put("/todos/{id}")
async def update_todos_title_by_id(id:int, todo:UpdateTodo):

    connection= get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            '''
            update todos set title = %s where id = %s
            ''' ,
            (todo.title,id)
        )

        connection.commit()

        return{
            "message": "todos updated successfully"
        }

    except Exception as e:
        return{
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


#DELETE TODOS
@app.delete("/todos/{id}")
async def delete_todos_by_id(id:int):

    connection=get_connection()
    cursor=connection.cursor()

    try:
        cursor.execute(
            '''
            delete from todos where id =%s
            ''',
            (id,)
        )

        connection.commit()

        return{
            "message": "todos deleted successfully"
        }

    except Exception as e:
        return{
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
    



    


    