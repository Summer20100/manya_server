# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt для установки зависимостей
COPY requirements.txt .

# Устанавливаем зависимости с помощью pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Указываем команду для запуска приложения (например, с использованием uvicorn для FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]

# Открываем порт для приложения
EXPOSE 4000
