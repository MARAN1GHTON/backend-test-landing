from fastapi import APIRouter
from app.repositories.file_storage import get_metrics

router = APIRouter()

@router.get("/metrics")
def metrics():
    """
    Получение статистики обращений.
    """
    return get_metrics()
