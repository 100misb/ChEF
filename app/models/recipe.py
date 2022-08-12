from pydantic import BaseModel
from typing import List

from app.services.clean_attributes import ingridients

class RecipeDetails(BaseModel):
    name: str
    description: str
    cuisine: str
    course: str
    diet: str
    ingridients: List[str]
    instruction: str


class RecipeDetailsResponse(BaseModel):
    name: str
    description: str
    cuisine: str
    course: str
    diet: str
    ingridients: List[str]
    instruction: List[List[str]]
    embeddings: List[float]