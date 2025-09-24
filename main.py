from fastapi import FastAPI
from src.api import router as chat_router

app = FastAPI(title="Recipe Recommendation API with Stateful Chat")

app.include_router(chat_router)