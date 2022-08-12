from typing import Any, List

import joblib
from app.core.errors import PredictException
from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from app.models.prediction import HealthResponse, MachineLearningResponse, RecipeRecommendation
from app.services.predict import MachineLearningModelHandlerScore as model
from app.services.predict import list_Similar_dishes
from typing import Union

router = APIRouter()

get_prediction = lambda data_input: MachineLearningResponse(
    model.predict(data_input, load_wrapper=joblib.load, method="predict_proba")
)


# @router.get("/predict", response_model=MachineLearningResponse, name="predict:get-data")
# async def predict(data_input: Any = None):
#     if not data_input:
#         raise HTTPException(status_code=404, detail=f"'data_input' argument invalid!")
#     try:
#         prediction = get_prediction(data_input)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Exception: {e}")

#     return MachineLearningResponse(prediction=prediction)


@router.get(
    "/health", response_model=HealthResponse, name="health:get-data",
)
async def health():
    is_health = False
    try:
        get_prediction("lorem ipsum")
        is_health = True
        return HealthResponse(status=is_health)
    except Exception:
        raise HTTPException(status_code=404, detail="Unhealthy")


@router.get("/predict"
# response_model=List[RecipeRecommendation]
)
async def predict(
    dish_number: int = Query(...),
    cuisine:  Union[List[str], None] = Query(None),
    diet: Union[List[str], None] = Query(None),
):
    print(cuisine)
    print(diet)

    res = await list_Similar_dishes(dish_number, cuisine, diet)
    return res
    
"""
Let me in
[11:48 pm, 05/08/2022] Susmita ISB: Indian
[11:48 pm, 05/08/2022] Susmita ISB: Andhra
[11:48 pm, 05/08/2022] Susmita ISB: Vegetarian

"""