from fastapi import FastAPI
from routes.vector_search import router

app = FastAPI(title="FastAPI Integration Test Example")
app.include_router(router=router)
