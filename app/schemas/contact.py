from pydantic import BaseModel, EmailStr, Field

class ContactRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Имя пользователя")
    phone: str = Field(..., min_length=10, max_length=20, description="Телефон пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    comment: str = Field(..., min_length=5, max_length=1000, description="Комментарий или сообщение")

class ContactResponse(BaseModel):
    status: str
    message: str
    ai_analysis: dict
