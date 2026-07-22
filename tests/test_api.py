import pytest
from unittest.mock import patch

@pytest.mark.asyncio
async def test_health_check(async_client):
    """
    Тест проверяет, что эндпоинт здоровья возвращает статус 200 и правильный JSON.
    """
    response = await async_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

@pytest.mark.asyncio
async def test_metrics(async_client):
    """
    Тест проверяет, что эндпоинт метрик возвращает статус 200 и структуру метрик.
    """
    response = await async_client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "requests" in data

@pytest.mark.asyncio
@patch("app.services.contact.analyze_and_generate_response")
@patch("app.services.contact.send_notification_to_owner")
@patch("app.services.contact.send_copy_to_user")
async def test_submit_contact_success(mock_send_user, mock_send_owner, mock_ai_analyze, async_client):
    """
    Успешная отправка контактной формы. Мы мокируем AI и отправку писем,
    чтобы не делать реальных вызовов к OpenAI и SMTP во время тестов.
    """
    # Настраиваем фейковый ответ от AI
    mock_ai_analyze.return_value = {
        "sentiment": "positive",
        "category": "collaboration",
        "auto_reply": "Спасибо за предложение, свяжусь с вами!"
    }

    payload = {
        "name": "Иван Иванов",
        "phone": "89991234567",
        "email": "ivan@example.com",
        "comment": "Отличный проект, хочу с вами работать."
    }

    response = await async_client.post("/api/contact", json=payload)
    
    # Проверяем, что запрос успешен
    assert response.status_code == 201
    data = response.json()
    
    assert data["status"] == "success"
    assert data["ai_analysis"]["sentiment"] == "positive"
    
    # Проверяем, что наши замокированные функции были вызваны
    mock_ai_analyze.assert_called_once_with(payload["comment"])
    mock_send_owner.assert_called_once_with(payload["name"], payload["email"], payload["comment"])
    mock_send_user.assert_called_once_with(payload["email"], "Спасибо за предложение, свяжусь с вами!")

@pytest.mark.asyncio
async def test_submit_contact_validation_error(async_client):
    """
    Тест проверяет, что при отправке неверного email возвращается ошибка 422.
    """
    payload = {
        "name": "И",  # Слишком короткое имя
        "phone": "123", # Слишком короткий телефон
        "email": "not-an-email", # Невалидный email
        "comment": "Тест"
    }

    response = await async_client.post("/api/contact", json=payload)
    
    # Ожидаем ошибку валидации от Pydantic (Unprocessable Entity)
    assert response.status_code == 422
    data = response.json()
    
    # В ответе должны быть детали об ошибках валидации
    assert "detail" in data
    assert isinstance(data["detail"], list)
