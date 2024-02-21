from typing import List

import pydantic as _pydantic


class _BookBase(_pydantic.BaseModel):
    title: str
    content: str


class BookCreate(_BookBase):
    pass


class Book(_BookBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class _WriterBase(_pydantic.BaseModel):
    email: str


class WriterCreate(_WriterBase):
    password: str


class Writer(_WriterBase):
    id: int
    books: List[Book] = []

    class Config:
        from_attributes = True
