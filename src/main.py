from fastapi import FastAPI

from src.core.config import settings

app = FastAPI(
    title="Alvin",
    version="0.1.0",
    debug=settings.app_debug,
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
