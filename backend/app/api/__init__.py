from fastapi import APIRouter

from .locations import router as locations_router
from .heatmap import router as heatmap_router

api_router = APIRouter()
api_router.include_router(locations_router, prefix="/locations", tags=["locations"])
api_router.include_router(heatmap_router, prefix="/heatmap", tags=["heatmap"])
