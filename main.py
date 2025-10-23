from fastapi import FastAPI
from routes.retrieve import router

app = FastAPI(title="FastAPI Integration Test Example")
app.include_router(router=router)
