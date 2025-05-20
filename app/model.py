import torch
from fastapi import HTTPException
from app.utils import logger
import whisper

class MLModel:
    def __init__(self, model_name: str):
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.load_model(model_name)

    def load_model(self, model_name: str):
        """Загрузка модели Whisper."""
        try:
            logger.info(f"Загружаем модель: {model_name}")
            self.model = whisper.load_model(model_name)
            logger.info("Модель успешно загружена")
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"Модель переведена на устройство: {self.device}")
        except Exception as e:
            logger.error(f"Ошибка загрузки модели: {str(e)}")
            raise Exception("Не удалось загрузить модель")

    def predict(self, path_to_file: str) -> str:
        """Предсказание текста на основе аудиофайла."""
        try:
            if not path_to_file.lower().endswith(('.wav', '.mp3', '.m4a')):
                raise HTTPException(400, "Поддерживаются только WAV, MP3 или M4A файлы")
            
            logger.info(f"Выполняется распознавание аудио: {path_to_file}")
            result = self.model.transcribe(path_to_file, language="ru")
            text_of_voice = result["text"].strip()
            logger.info(f"Предсказанный текст: {text_of_voice}")
            return text_of_voice
        except Exception as e:
            logger.error(f"Ошибка распознавания: {str(e)}")
            raise HTTPException(500, f"Ошибка модели: {str(e)}")