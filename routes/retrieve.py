from fastapi import APIRouter
from models.book import Book

router = APIRouter()

@router.post("/retrieve", tags=["retrieve"])
async def retrieve()
