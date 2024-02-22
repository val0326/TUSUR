import database as _database
import models as _models
import schemas as _schemas
import sqlalchemy.orm as _orm


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_book(
    db: _orm.Session,
    book: _schemas.BookCreate,
):
    book = _models.Book(**book.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books(db: _orm.Session, skip: int, limit: int):
    return db.query(_models.Book).offset(skip).limit(limit).all()


def get_book(db: _orm.Session, book_id: int):
    return db.query(_models.Book).filter(_models.Book.id == book_id).first()


def delete_book(db: _orm.Session, book_id: int):
    db.query(_models.Book).filter(_models.Book.id == book_id).delete()
    db.commit()


def update_book(db: _orm.Session, book: _schemas.BookCreate, book_id: int):
    db_book = get_book(db=db, book_id=book_id)
    db_book.title = book.title
    db_book.content = book.content
    db.commit()
    db.refresh(db_book)
    return db_book
