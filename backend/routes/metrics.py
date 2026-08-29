from fastapi import APIRouter

from backend.services.metrics_service import get_metrics_summary

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"],
)


@router.get("/")
def get_metrics():
    return get_metrics_summary()