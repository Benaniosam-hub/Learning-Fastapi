from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self,id,title,author,description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed to create", default=None)
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=1,max_length=50)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1,lt=6)
    published_date: int 

    model_config = {
        "json_schema_extra": {
            "example":{
                "id": 0,
                "title": "A new book",
                "author": "unknown",
                "description": "A new description of a book",
                "rating":5,
                "published_date": 2026
            }
        }
    }

BOOKS = [
    Book(1, 'Mathematics', 'Benaniosam', 'Cool Solutions!', 5, 2020),
    Book(2, 'Computer Science', 'Joshua', 'AI Advanced!', 4, 2023),
    Book(3, 'FastAPI', 'Robby', 'New Methods Involved!', 5, 2024),
    Book(4, 'Social Science', 'Adam', 'Improved Version!', 4, 2025),
    Book(5, 'Algebra', 'Benaniosam', 'Cool Solutions Included!', 5, 2021),
    Book(6, 'HP1', 'Author 1', 'Book description', 3, 2026)
]


@app.get("/books2")
async def read_all_books():
    return BOOKS

@app.get("/books2/by_rating") #Query parameter
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    return_book = []
    for book in BOOKS:
        if book.rating == book_rating:
            return_book.append(book)
    return return_book

@app.get("/books2/by_date")
async def read_book_by_published_date(date: int = Query(gt=1999,lt=2031)):
    given_book = []
    for book in BOOKS:
        if book.published_date == date:
            given_book.append(book)
    return given_book 

@app.get("/books2/{id}") #Path parameter
async def read_book(id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')

@app.post("/books2/create-book")
async def create_book(book_added: BookRequest):
    new_book=Book(**book_added.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book): 
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put("/books2/update_book")
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i]=book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')

@app.delete("/books2/{delete_book_id}")
async def delete_book(delete_book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == delete_book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')