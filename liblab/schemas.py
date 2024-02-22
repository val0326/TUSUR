import pydantic as _pydantic


class _BookBase(_pydantic.BaseModel):
    title: str
    content: str


class BookCreate(_BookBase):
    pass


class Book(_BookBase):
    id: int

    class Config:
        from_attributes = True
