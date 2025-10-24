from pydantic import BaseModel, Field, field_validator
from typing import Optional
from .book import Category
import re

class Filters(BaseModel):
    category: Optional[Category] = None
    isbn: Optional[str] = None
    author: Optional[str] = Field(default=None, min_length=1)

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        clean = v.replace("-", "")
        if not (re.fullmatch(r"\d{10}", clean) or re.fullmatch(r"\d{13}", clean)):
            raise ValueError("isbn must be ISBN-10 or ISBN-13 (digits/dashes)")

        return v

    @field_validator("author")
    @classmethod
    def normalize_author(cls, v: Optional[str]) -> Optional[str]:
        return None if v is None else v.strip()
