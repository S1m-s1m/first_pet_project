FROM python:3.10

# Установите рабочую директорию
WORKDIR /usr/src/app

# Скопируйте файл зависимостей в контейнер
ADD requirements.txt /usr/src/app/requirements.txt

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте все файлы в рабочую директорию
COPY . .

# Укажите команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]