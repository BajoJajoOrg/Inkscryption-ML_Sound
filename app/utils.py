import logging
import os
import tempfile
from fastapi import HTTPException, UploadFile
from app.config import Config

# Настройка логирования
if not os.path.exists(Config.LOG_DIR):
    os.makedirs(Config.LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

async def save_uploaded_audio(audio_file: UploadFile) -> str:
    """Сохранение загруженного аудиофайла во временный файл."""
    try:
        # Проверка Content-Type
        # content_type = audio_file.content_type
        # if content_type not in ['audio/wav', 'audio/mpeg', 'audio/mp4']:
        #     raise HTTPException(400, "Поддерживаются только WAV, MP3 или M4A файлы")
        
        # Проверка размера файла (например, до 50 MB)
        max_size = 50 * 1024 * 1024  # 50 MB
        content = await audio_file.read()
        if len(content) > max_size:
            raise HTTPException(400, "Файл слишком большой, максимум 50 MB")
        
        # Проверка расширения файла
        filename = audio_file.filename.lower()
        if not filename.endswith(('.wav', '.mp3', '.m4a')):
            raise HTTPException(400, "Недопустимое расширение файла")
        
        # Сохранение во временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        logger.info(f"Аудиофайл сохранен как: {temp_file_path}")
        return temp_file_path
    except Exception as e:
        logger.error(f"Ошибка обработки аудиофайла: {str(e)}")
        raise HTTPException(status_code=400, detail="Ошибка при обработке аудиофайла")