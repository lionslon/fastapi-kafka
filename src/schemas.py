from pydantic import BaseModel
from datetime import datetime


# Схема для валидации входных данных
class DataEntryCreate(BaseModel):
    content: str


# Схема для ответа при запросе
class DataEntryCreateResponse(BaseModel):
    id: int
    message: str


# Схема для ответа при получении
class DataEntryResponse(BaseModel):
    id: int
    content: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True
