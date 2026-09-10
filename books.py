from fastapi import Body, FastAPI

app = FastAPI() # this allows uvicorn to identify that we create new fastapi 

BOOKS = [
    {'id':1,'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'id':2,'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'id':3,'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'id':4,'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'id':5,'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'id':2,'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

# GET INVOLVES TWO METHODS, PATH AND QUERY
@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/book/{id}") #PATH PARAMETER
async def get_book_by_id(id: int):
    for book in BOOKS:
        if book.get('id') == id:
            return book


@app.get("/book/")  #QUERY PARAMETER
async def read_category_by_query(category: str):
    books = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books.append(book)
    return books


# POST METHOD TO CREATE NEW BOOK
@app.post("/book/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


# PUT METHOD FOR UPDATE BOOKS
@app.put("/book/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('id') == updated_book.get('id'):
            BOOKS[i]=updated_book


# DELETE IS TO DELETE THE EXISTING BOOKS BY ID
@app.delete("/book/{id}")
async def delete_book(id: int):
    for x in range(len(BOOKS)):
        if BOOKS[x].get('id') == id:
            BOOKS.pop(x)
            break
        return f"message: the book id {id} has been removed successfully"
    
@app.get("/books/{author}")
async def get_books_from_specific_author(author:str):
    author_book=[]
    for e in BOOKS:
        if e.get('author') == author:
            author_book.append(e)
    return author_book