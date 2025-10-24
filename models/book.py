from pydantic import BaseModel, conlist
from enum import Enum

class Category(str, Enum):
    SCIFI = "scifi"
    HORROR = "horror"
    MYSTERY = "mystery"
    BIO = "biography"
    ROMANCE = "romance"

class Book(BaseModel):
    id: str
    isbn: str
    chapter: int
    title: str
    chunk_text: str
    author: str
    category: Category
    vector: conlist(float, min_length=384, max_length=384) # type: ignore[misc]
