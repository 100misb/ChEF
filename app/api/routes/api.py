from fastapi import APIRouter

from app.api.routes import predictor
from app.api.routes import recipe
from app.api.routes import feedback

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"], prefix="/v1/predict")
router.include_router(recipe.router, tags=["recipe"], prefix="/v1/recipe")
router.include_router(feedback.router,tags=["feedback"], prefix="/v1/feedback")