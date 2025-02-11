import json

from aiokafka.errors import KafkaError
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from aiokafka import AIOKafkaProducer

from .config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from .models import DataEntry
from .database import async_session
from loguru import logger

from .schemas import DataEntryCreate, DataEntryCreateResponse, DataEntryResponse

router = APIRouter()


# Endpoint для добавления данных
@router.post("/data", response_model=DataEntryCreateResponse)
async def create_data_entry(data: DataEntryCreate) -> DataEntryCreateResponse:
    """Создаем новую запись в БД и публикуем данные в Kafka"""
    async with async_session() as session:
        try:
            new_entry = DataEntry(content=data.content)
            session.add(new_entry)
            await session.commit()
            await session.refresh(new_entry)
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Unexpected error")
        logger.info(f"Успешно записали в БД данные с ID: {new_entry.id}")
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
        try:
            message = {"id": new_entry.id, "content": new_entry.content}
            logger.info(f"Отправка {message=} в Kafka топик: {KAFKA_TOPIC}")
            await producer.send_and_wait(KAFKA_TOPIC, json.dumps(message).encode('utf-8'))
        except KafkaError as e:
            logger.error(f"Получена ошибка при отправке в Kafka: {str(e)}")
            raise HTTPException(status_code=502, detail=f"{e}")
        finally:
            await producer.stop()
            logger.info(f"Сообщение было отправлено в Kafka - {message}")
            return DataEntryCreateResponse(
                id=new_entry.id,
                message="Data saved and published to Kafka.",
            )


# Endpoint для получения всех данных
@router.get("/data", response_model=list[DataEntryResponse])
async def get_all_data() -> DataEntryResponse:
    """Получение данных из БД"""
    async with async_session() as session:
        try:
            result = await session.execute(select(DataEntry))
            entries = result.scalars().all()
            return entries
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Unexpected error")
