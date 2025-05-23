# Базовый образ с CUDA 12.8 (только runtime)
FROM nvidia/cuda:12.3.2-runtime-ubuntu22.04

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    python3.11 python3.11-venv python3.11-dev \
    python3-pip \
    ffmpeg git curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка pip и обновление
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Используем python3.11 по умолчанию
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Установка PyTorch и зависимостей через официальный индекс CUDA 12.8
RUN pip install --upgrade pip
RUN pip install torch==2.7.0+cu128 \
                torchaudio==2.7.0+cu128 \
                torchvision==0.22.0+cu128 \
                --index-url https://download.pytorch.org/whl/cu128

# Копируем зависимости и устанавливаем Python-библиотеки
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY ./app /app/app

# Указываем порт
EXPOSE 7000

# Запуск FastAPI через uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000"]