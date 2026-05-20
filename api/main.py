from fastapi import FastAPI

from api.routes.health import router as health_router
from api.routes.insights import router as insights_router
from api.routes.kpis import router as kpis_router

app = FastAPI(
    title="FitConnect Analytics Platform API",
    version="0.1.0",
    description="Analytics API for FitConnect Hub product metrics and AI insights.",
)

app.include_router(health_router)
app.include_router(kpis_router)
app.include_router(insights_router)