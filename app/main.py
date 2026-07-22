from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import contact, health, metrics
from app.core.exceptions import RateLimitExceeded, rate_limit_handler, global_exception_handler
from app.core.logger import logger
import os

app = FastAPI(
    title="Developer Landing API",
    description="Backend API для формы обратной связи разработчика с интеграцией AI",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене следует указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Обработчики исключений
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Подключение роутеров
app.include_router(contact.router, prefix="/api", tags=["Contact"])
app.include_router(health.router, prefix="/api", tags=["System"])
app.include_router(metrics.router, prefix="/api", tags=["System"])

# Раздача статических файлов (Frontend)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

logger.info("Application startup complete.")
