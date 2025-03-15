from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import config
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# Строка подключения к БД
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{config.user}:{config.password}@{config.host}:{config.port}/{config.dbname}"
)

# Создание асинхронного движка с параметрами пула
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_size=30,       # Максимальное количество соединений
    max_overflow=50,    # Максимальный размер очереди соединений
    pool_recycle=1800,  # Закрытие неактивных соединений (30 минут)
    pool_pre_ping=True  # Проверка соединения перед использованием
)

# Фабрика сессий
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

# Зависимость для получения сессии БД
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

# Контекст жизненного цикла приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()  # Закрытие соединений при завершении

# Создание FastAPI-приложения
app = FastAPI(lifespan=lifespan)

# Настройки CORS
""" app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) """

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173" , 
        "http://localhost:5174" ,
        "http://localhost:5175" ,
        "https://marusina-sweets.vercel.app",
        "https://marusina-sweets-admin.vercel.app",
        "https://marusina-sweets-dj9l.onrender.com"
    ],  # ✅ Указываем конкретный origin
    allow_credentials=True,  # ✅ Разрешаем передачу credentials (cookies, токены)
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Разрешаем все заголовки
)
