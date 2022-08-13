from typing import Callable
import boto3
from fastapi import FastAPI
from app.core.config import Settings
from loguru import logger

settings = Settings()

def preload_model():
    """
    In order to load model on memory to each worker
    """
    from services.predict import MachineLearningModelHandlerScore

    MachineLearningModelHandlerScore.get_model()


def get_data_file_from_s3():
    s3 = boto3.client("s3", region_name='ap-south-1')
    s3.download_file(
        "chef-foods", "df_indianRecipes.pkl", settings.DATA_FILE_PATH
    )


def get_model_from_s3():
    s3 = boto3.client("s3", region_name='ap-south-1')
    s3.download_file(
        "chef-foods", "model_indianfood_fasttext.model", settings.FAST_TEXT_EMBEDDINGS
    )


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        preload_model()

    return start_app


def save_data_locally(app: FastAPI) -> Callable:
    def download_data_file() -> None:
        get_data_file_from_s3()
        logger.info("Dataset File downloaded successfully")

    return download_data_file()

def save_model_locally(app: FastAPI) -> Callable:
    def download_model_file() -> None:
        get_model_from_s3()
        logger.info("Model file Downloaded succesfully")

    return download_model_file()

