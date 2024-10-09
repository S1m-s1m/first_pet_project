FROM python:3.11

# Установка рабочей директории
WORKDIR /usr/src/app

# Копирование файла зависимостей и установка зависимостей
COPY requirements.txt /usr/src/app/
RUN apt-get update && \
    apt-get install -y \
    libffi-dev \
    libpango1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    ghostscript \
    openssl && \
    apt-get clean

RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов
COPY . .

# Запуск приложения Django
CMD ["gunicorn", "pet_project.wsgi:application", "--bind", "0.0.0.0:8000"]

