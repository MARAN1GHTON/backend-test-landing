from app.core.logger import logger
from app.core.config import settings

def send_notification_to_owner(name: str, email: str, comment: str):
    logger.info(f"Mock Email sent to owner {settings.ADMIN_EMAIL} from {name} ({email})")

def send_copy_to_user(email: str, ai_response: str):
    logger.info(f"Mock Email sent to user {email}. Content: {ai_response}")
