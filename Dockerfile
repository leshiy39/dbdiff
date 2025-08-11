# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем зависимости системы (например, для psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем зависимости (если requirements.txt есть)
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники приложения
COPY . .

# Указываем переменную окружения для Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Открываем порт (например, 5000)
EXPOSE 5000

# Запуск приложения
CMD ["flask", "run"]
