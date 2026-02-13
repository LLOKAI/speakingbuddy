"""SpeakingBuddy FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routes import categories, words, audio, pronunciation


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    await init_db()
    yield


app = FastAPI(
    title="SpeakingBuddy API",
    description="Luxembourgish pronunciation learning backend",
    version="0.1.0",
    lifespan=lifespan,
)

# ── CORS ────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ──────────────────────────────────────────────────
app.include_router(categories.router, prefix="/api")
app.include_router(words.router, prefix="/api")
app.include_router(audio.router, prefix="/api")
app.include_router(pronunciation.router, prefix="/api")


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
