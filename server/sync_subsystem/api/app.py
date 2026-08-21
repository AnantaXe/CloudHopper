from __future__ import annotations

from fastapi import FastAPI
from prometheus_client import make_asgi_app

from .routes import router
from .dependencies import repository

app = FastAPI(title="CloudHopper Sync Subsystem", version="0.1.0")
app.include_router(router)
app.mount("/metrics", make_asgi_app())


@app.on_event("startup")
async def startup_event() -> None:
    await repository.connect()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await repository.close()
