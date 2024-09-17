# FROM python:3.11

# RUN apt-get update && apt-get install -y curl unzip

# # Установите рабочую директорию
# WORKDIR /usr/src/app

# # Скопируйте файл зависимостей в контейнер
# ADD requirements.txt /usr/src/app/requirements.txt

# # Установите зависимости
# # RUN pip install --no-cache-dir -r requirements.txt || tail -n 20 /root/.pip/pip.log
# RUN pip install --no-cache-dir -r requirements.txt 

# # Скопируйте все файлы в рабочую директорию
# COPY . .

# # Установка ngrok
# RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc > /dev/null && \
#     echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
#     apt-get update && apt-get install ngrok -y

# # Укажите команду для запуска приложения
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "ngrok http 8000"]

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

# Установка ngrok
RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc > /dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install -y ngrok

# Копирование остальных файлов
COPY . .

# Запуск приложения Django
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "pet_project.wsgi:application", "--bind", "0.0.0.0:8000"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "openssl s_client -starttls smtp -connect 2007kim.maksim@gmail.com:587 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > /certificates.pem && python app.py"]

