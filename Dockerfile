# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Обновляем pip
RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y libpq-dev


# Копируем requirements.txt для установки зависимостей
COPY requirements.txt .

# Устанавливаем зависимости с помощью pip
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Указываем команду для запуска приложения (например, с использованием uvicorn для FastAPI)
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:4000"]

# Открываем порт для приложения
EXPOSE 4000
