from fastapi import FastAPI, HTTPException, UploadFile, File
from app.model import MLModel
from app.utils import logger, save_uploaded_audio
from app.config import Config

app = FastAPI(title="ML Audio-to-Text Service")

# Инициализация модели
try:
    ml_model = MLModel(Config.MODEL_PATH)
except Exception as e:
    logger.critical(f"Не удалось запустить сервис: {str(e)}")
    raise e

@app.post("/predict/", response_model=dict)
async def predict(audio_file: UploadFile = File(...)):
    """Эндпоинт для предсказания текста из загруженного аудиофайла."""
    logger.info(f"Получен запрос на предсказание, файл: {audio_file.filename}")
    
    # Сохраняем загруженный файл во временный файл
    try:
        audio_path = await save_uploaded_audio(audio_file)
    except HTTPException as e:
        logger.error(f"Ошибка обработки файла: {str(e)}")
        raise e
    
    # Получаем предсказание
    try:
        text = ml_model.predict(audio_path)
        return {"text": text}
    finally:
        # Удаляем временный файл
        import os
        if os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info(f"Временный файл удален: {audio_path}")

@app.get("/health")
async def health_check():
    """Проверка состояния сервиса."""
    return {"status": "healthy"}