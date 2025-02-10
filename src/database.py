from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .models import Base
from .config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Инициализация базы данных  
async def init_db():  
    async with engine.begin() as conn:  
        await conn.run_sync(Base.metadata.create_all)
