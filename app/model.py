import torch
from fastapi import HTTPException
from app.utils import logger
import whisper

import os
ffmpeg_path = r"C:\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"
os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ["PATH"]


class MLModel:
    def __init__(self):
        self.processor = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.load_model()

    def load_model(self):
        """Загрузка процессора и модели."""
        try:
            logger.info(f"Загружаем модель")
            self.model = whisper.load_model("large")
            logger.info("Модель успешно загружена")
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"Модель переведена на устройство: {self.device}")
        except Exception as e:
            logger.error(f"Ошибка загрузки модели: {str(e)}")
            raise Exception("Не удалось загрузить модель")

    def predict(self, path_to_file: str) -> str:
        """Предсказание текста на основе изображения."""
        try:
            logger.info("Выполняется распознавание")
            result = self.model.transcribe(path_to_file, language="ru")
            text_of_voice = result["text"]
            logger.info(f"Предсказанный текст: {text_of_voice}")
            return text_of_voice
        except Exception as e:
            logger.error(f"Ошибка распознавания: {str(e)}")
            # Исправляем синтаксис HTTPException
            raise HTTPException(500, "Ошибка модели")