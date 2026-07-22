from app.schemas.contact import ContactRequest, ContactResponse
from app.services.ai import analyze_and_generate_response
from app.services.email import send_notification_to_owner, send_copy_to_user
from app.repositories.file_storage import save_contact_request

async def process_contact_request(request: ContactRequest) -> ContactResponse:
    # 1. Анализ текста AI и генерация автоответа
    ai_result = await analyze_and_generate_response(request.comment)
    
    # 2. Отправка писем (Заглушка)
    send_notification_to_owner(request.name, request.email, request.comment)
    send_copy_to_user(request.email, ai_result["auto_reply"])
    
    # 3. Сохранение запроса для статистики
    save_contact_request({
        "name": request.name,
        "email": request.email,
        "sentiment": ai_result["sentiment"]
    })
    
    # 4. Возврат ответа клиенту
    return ContactResponse(
        status="success",
        message="Ваша заявка успешно отправлена.",
        ai_analysis=ai_result
    )
