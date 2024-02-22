from typing import List

import fastapi as _fastapi
import schemas as _schemas
import services as _services
import sqlalchemy.orm as _orm


app = _fastapi.FastAPI()

_services.create_database()


@app.post("/books/", response_model=_schemas.Book)
def create_book(
    book: _schemas.BookCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.create_book(db=db, book=book)


@app.get("/books/", response_model=List[_schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    books = _services.get_books(db=db, skip=skip, limit=limit)
    return books


@app.get("/books/{book_id}", response_model=_schemas.Book)
def read_book(
    book_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    book = _services.get_book(db=db, book_id=book_id)
    if book is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this book does not exist"
        )
    return book


@app.delete("/books/{book_id}")
def delete_book(
    book_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    _services.delete_book(db=db, book_id=book_id)
    return {"message": f"successfully deleted book with id: {book_id}"}


@app.put("/books/{book_id}", response_model=_schemas.Book)
def update_book(
    book_id: int,
    book: _schemas.BookCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.update_book(db=db, book=book, book_id=book_id)
