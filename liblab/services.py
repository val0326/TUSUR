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


def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()


def create_user(db: _orm.Session, user: _schemas.UserCreate):
    fake_hashed_password = user.password + "thisisnotsecure"
    db_user = _models.User(
        email=user.email, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: _orm.Session, skip: int, limit: int):
    return db.query(_models.User).offset(skip).limit(limit).all()


def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()


def create_book(db: _orm.Session, book: _schemas.BookCreate, user_id: int):
    book = _models.Book(**book.model_dump(), owner_id=user_id)
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


def delete_user(db: _orm.Session, user_id: int):
    db.query(_models.User).filter(_models.User.id == user_id).delete()
    db.commit()


def update_book(db: _orm.Session, book: _schemas.BookCreate, book_id: int):
    db_book = get_book(db=db, book_id=book_id)
    db_book.title = book.title
    db_book.content = book.content
    # db_post.date_last_updated = _dt.datetime.now()
    db.commit()
    db.refresh(db_book)
    return db_book
