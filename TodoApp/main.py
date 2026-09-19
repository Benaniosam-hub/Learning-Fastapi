from fastapi import FastAPI
from Todo import todos
import models
from Todo.database import engine
from routers import auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
