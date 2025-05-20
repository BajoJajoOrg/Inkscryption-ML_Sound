# Базовый образ
FROM python:3.11-slim

# Установка ffmpeg
RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

# Рабочая директория
WORKDIR /app

RUN pip install torch==2.7.0+cu128 \
                torchaudio==2.7.0+cu128 \
                torchvision==0.22.0+cu128 \
                --index-url https://download.pytorch.org/whl/cu128

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY ./app /app/app

# Указываем порт
EXPOSE 7000

# Команда для запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000"]