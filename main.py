from fastapi import FastAPI
from routes.vector_search import router as vector_router
from routes.health import router as health_router

app = FastAPI(title="FastAPI Integration Test Example")
app.include_router(router=vector_router)
app.include_router(router=health_router)
