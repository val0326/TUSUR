import database as _database
import sqlalchemy as _sql
import sqlalchemy.orm as _orm


class Writer(_database.Base):
    __tablename__ = "writers"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    # hashed_password = _sql.Column(_sql.String)
    # is_active = _sql.Column(_sql.Boolean, default=True)

    books = _orm.relationship("Book", back_populates="owner")


class Book(_database.Base):
    __tablename__ = "books"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    content = _sql.Column(_sql.String, index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("writers.id"))

    owner = _orm.relationship("Writer", back_populates="books")
