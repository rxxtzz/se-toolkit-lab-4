from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.auth import verify_api_key
from backend.app.routers import interactions, items, learners
from backend.app.settings import settings
from app.routers import interactions, items, learners
from app.settings import settings

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(items.router, prefix="/api/items", tags=["items"])
app.include_router(learners.router, prefix="/api/learners", tags=["learners"])
app.include_router(interactions.router, prefix="/api/interactions", tags=["interactions"])

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
