import datetime as _dt
from typing import List

import pydantic as _pydantic


class _BookBase(_pydantic.BaseModel):
    title: str
    content: str


class BookCreate(_BookBase):
    pass


class Book(_BookBase):
    id: int

    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        from_attributes = True
