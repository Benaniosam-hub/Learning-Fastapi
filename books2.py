from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self,id,title,author,description,rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=1,max_length=50)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1,lt=6)

BOOKS = [
    Book(1, 'Mathematics', 'Benaniosam', 'Cool Solutions!', 5),
    Book(2, 'Computer Science', 'Joshua', 'AI Advanced!', 4),
    Book(3, 'FastAPI', 'Robby', 'New Methods Involved!', 5),
    Book(4, 'Social Science', 'Adam', 'Improved Version!', 4),
    Book(5, 'Algebra', 'Benaniosam', 'Cool Solutions Included!', 5),
    Book(6, 'HP1', 'Author 1', 'Book description', 3)
]


@app.get("/books2")
async def read_all_books():
    return BOOKS

@app.post("/create-book")
async def create_book(book_added: BookRequest):
    new_book=Book(**book_added.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book
