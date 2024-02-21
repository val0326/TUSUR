from typing import List

import fastapi as _fastapi
import schemas as _schemas
import services as _services
import sqlalchemy.orm as _orm


app = _fastapi.FastAPI()

_services.create_database()


@app.post("/users/", response_model=_schemas.User)
def create_user(
    user: _schemas.UserCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="woops the email is in use"
        )
    return _services.create_user(db=db, user=user)


@app.get("/users/", response_model=List[_schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    users = _services.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=_schemas.User)
def read_user(
    user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )
    return db_user


@app.post("/users/{user_id}/books/", response_model=_schemas.Book)
def create_book(
    user_id: int,
    book: _schemas.BookCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )
    return _services.create_book(db=db, book=book, user_id=user_id)


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


@app.delete("/users/{user_id}")
def delete_user(
    user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    _services.delete_user(db=db, user_id=user_id)
    return {"message": f"successfully deleted user with id: {user_id}"}


@app.put("/books/{book_id}", response_model=_schemas.Book)
def update_book(
    book_id: int,
    book: _schemas.BookCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.update_book(db=db, book=book, book_id=book_id)
