import logging
import sys
from typing import List

from app.core.logging import InterceptHandler
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from pydantic import BaseSettings
from pathlib import Path

config_file_path = Path(__file__).resolve()
root_dir = config_file_path.parents[2]
app_dir = config_file_path.parents[1]


config = Config(".env")

API_PREFIX = "/api"
VERSION = "0.1.0"
DEBUG: bool = config("DEBUG", cast=bool, default=False)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="")

PROJECT_NAME: str = config("PROJECT_NAME", default="chef")

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

MODEL_PATH = config("MODEL_PATH", default="./ml/model/")
MODEL_NAME = config("MODEL_NAME", default="model.pkl")


class Settings(BaseSettings):

    # DATA_FILE_PATH: str = "/home/somi/ampba/fp1/chef/data/external/df_indianRecipes.pkl"
    # FAST_TEXT_EMBEDDINGS: str = "/home/somi/ampba/fp1/chef/nlp/models/model_indianfood_fasttext.model"

    DATA_FILE_PATH: str = str(app_dir / "data" / "df_indianRecipes.pkl")
    FAST_TEXT_EMBEDDINGS: str = str(root_dir/ "app" / "ml" / "model" / "model_indianfood_fasttext.model")
    DEFAULT_RECIPE_IMAGE: str = str(app_dir / "data" / "blank_image.jpg")
    FEEDBACK_FILE : Path = app_dir / "data" / "feedback.json"
    # LOCALHOST_SEED_URL: str = "http://localhost:"
    # PORT: str = "8000"
