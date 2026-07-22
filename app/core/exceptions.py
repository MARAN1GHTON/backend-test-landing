from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logger import logger

class RateLimitExceeded(Exception):
    pass

async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(f"Rate limit exceeded for IP: {request.client.host}")
    return JSONResponse(
        status_code=429,
        content={"detail": "Слишком много запросов. Пожалуйста, подождите немного перед следующей отправкой."}
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера. Мы уже работаем над её устранением."}
    )
