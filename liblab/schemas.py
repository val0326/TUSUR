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


class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    password: str


class User(_UserBase):
    id: int
    is_active: bool
    posts: List[Book] = []

    class Config:
        from_attributes = True
