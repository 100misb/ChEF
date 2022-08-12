from pydantic import BaseModel
from typing import Optional, List


class MachineLearningResponse(BaseModel):
    prediction: float


class HealthResponse(BaseModel):
    status: bool

class RecipeRecommendation(BaseModel):
    TranslatedRecipeName: str
    Cuisine: str
    Course: str
    Diet: str
    clean_ingredients : List[str]