FROM python:3.11-slim

WORKDIR /app

# 1. Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Установка Poetry
RUN pip install --no-cache-dir poetry

# 3. Копируем ТОЛЬКО файлы зависимостей (для кэширования слоя)
COPY pyproject.toml poetry.lock ./

# 4. Устанавливаем Python-зависимости (этот слой закэшируется, пока не изменится pyproject.toml)
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# 5. ТЕПЕРЬ копируем весь исходный код проекта
COPY . .

# 6. Запускаем Django-команды, используя окружение Poetry
RUN poetry run python manage.py collectstatic --noinput

EXPOSE 8000

# 7. Запуск сервера
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]