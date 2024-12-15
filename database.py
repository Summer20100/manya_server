from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config
from contextlib import asynccontextmanager

# Строка подключения
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{config.user}:{config.password}@{config.host}:{config.port}/{config.dbname}"

# Создание асинхронного движка
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Сессия для работы с БД
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для моделей
Base = declarative_base()

# Инициализация базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Получение сессии БД
async def get_db():
    async with SessionLocal() as db:
        yield db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    print("Shutdown process")

app = FastAPI(lifespan=lifespan)
