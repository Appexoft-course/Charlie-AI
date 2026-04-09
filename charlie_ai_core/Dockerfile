# Використовуємо легкий офіційний образ Python
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Змінні середовища для оптимізації Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Встановлюємо Poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Копіюємо файли залежностей
COPY pyproject.toml poetry.lock* ./

# Налаштовуємо Poetry: не створювати virtualenv, оскільки контейнер вже ізольований
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копіюємо весь код проєкту
COPY . .

# Команда для запуску FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]