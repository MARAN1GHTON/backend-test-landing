from fastapi import APIRouter, Depends, Request
from app.schemas.contact import ContactRequest, ContactResponse
from app.services.contact import process_contact_request
from app.api.dependencies import check_rate_limit
from app.core.logger import logger

router = APIRouter()

@router.post("/contact", response_model=ContactResponse, status_code=201, dependencies=[Depends(check_rate_limit)])
async def submit_contact(request: Request, contact_data: ContactRequest):
    """
    Эндпоинт для отправки формы обратной связи.
    """
    logger.info(f"Received contact request from {contact_data.email} (IP: {request.client.host})")
    response = await process_contact_request(contact_data)
    return response
