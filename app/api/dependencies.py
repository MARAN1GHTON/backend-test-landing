from fastapi import Request
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.exceptions import RateLimitExceeded
import json
import os

RATE_LIMIT_FILE = "data/rate_limits.json"

def _load_limits():
    if not os.path.exists(RATE_LIMIT_FILE):
        return {}
    with open(RATE_LIMIT_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def _save_limits(data):
    with open(RATE_LIMIT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f)

async def check_rate_limit(request: Request):
    """
    Простой Rate Limiter на основе JSON-файла.
    Проверяет, сколько запросов сделал IP за последнюю минуту.
    """
    client_ip = request.client.host
    now = datetime.utcnow()
    
    limits = _load_limits()
    
    # Очистка старых записей
    limits = {
        ip: [time_str for time_str in timestamps if (now - datetime.fromisoformat(time_str)) < timedelta(minutes=1)]
        for ip, timestamps in limits.items()
    }
    
    user_requests = limits.get(client_ip, [])
    
    if len(user_requests) >= settings.RATE_LIMIT_PER_MINUTE:
        _save_limits(limits)
        raise RateLimitExceeded()
        
    user_requests.append(now.isoformat())
    limits[client_ip] = user_requests
    
    _save_limits(limits)
