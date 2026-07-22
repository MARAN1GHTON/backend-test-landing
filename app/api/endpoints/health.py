from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    """
    Проверка статуса сервиса (Liveness/Readiness probe).
    """
    return {"status": "ok"}
