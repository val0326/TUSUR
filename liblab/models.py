import datetime as _dt

import database as _database
import sqlalchemy as _sql
import sqlalchemy.orm as _orm


class Book(_database.Base):
    __tablename__ = "books"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    content = _sql.Column(_sql.String, index=True)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
