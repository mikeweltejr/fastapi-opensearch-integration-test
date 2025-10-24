from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/health")
def health() -> str:
    return "Healthy"
