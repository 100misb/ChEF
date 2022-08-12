from typing import Any, List

from fastapi import APIRouter, HTTPException, Query
from app.services.clean_attributes import ingridients
from loguru import logger
from app.models.recipe import RecipeDetails, RecipeDetailsResponse
from app.services import clean_attributes
from gensim.test.utils import get_tmpfile
from gensim.models import FastText
from app.core.config import Settings
from app.services.predict import list_Similar_dishes, list_similar_dishes_by_name
from app.services.recipe import get_recipe_detail_by_id, get_recipe_detail_by_name


import pandas as pd
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


FASTTEXT_MODEL_PATH = "/home/somi/ampba/fp1/chef/nlp/models/model_indianfood_fasttext.model"
settings = Settings()

router = APIRouter()

# fasttext_model_file = get_tmpfile(FASTTEXT_MODEL_PATH)
# fasttext_model = FastText.load(fasttext_model_file)
fasttext_model = ...

@router.post(
    "/",
    response_model=RecipeDetailsResponse
)
async def save_recipe(
    recipe_detail_schema: RecipeDetails
):
    cleaned_ingridients = clean_attributes.ingridients(recipe_detail_schema.ingridients)
    cleaned_instructions = clean_attributes.instruction(recipe_detail_schema.instruction)
    embeddings = clean_attributes.embeddings(cleaned_instructions, fasttext_model)
    return {
        "name": recipe_detail_schema.name,
        "description": recipe_detail_schema.description,
        "cuisine": recipe_detail_schema.cuisine,
        "course": recipe_detail_schema.course,
        "diet": recipe_detail_schema.diet,
        "ingridients": cleaned_ingridients,
        "instruction": cleaned_instructions,
        "embeddings": embeddings.tolist()
    }


@router.get(
    "/"
)
async def get_recipies(
    course: List[str] = Query([]),
    diet: List[str] = Query([]),
    cuisine: List[str] = Query([])
):  
    # provide functionality to filter of the dataset on various queries
    cleaned_data = pd.read_pickle(
        settings.DATA_FILE_PATH
    )
    # print(cleaned_data.shape)
    if not course:
        course = cleaned_data.Course.unique().tolist()
    if not cuisine:
        cuisine = cleaned_data.Cuisine.unique().tolist()
    if not diet:
        diet = cleaned_data.Diet.unique().tolist()
    
    mask_df = cleaned_data[
        (cleaned_data["Course"].isin(course)) &
        (cleaned_data["Diet"].isin(diet)) &
        (cleaned_data["Cuisine"].isin(cuisine))
    ]
    mask_df = mask_df[["TranslatedRecipeName","TranslatedIngredients", "Cuisine", "Course", "Diet", "URL"]]
    return mask_df.to_dict(orient="records")


@router.get(
    "/{recipe_id}",
)
async def get_recipe_details(
    recipe_id: int,
    cuisine: List[str] = Query(None),
    diet: List[str] = Query(None),
    with_recommendations: bool = True,
):
    
    # base recipe informations should be independent from its recommendations
    recipe_details = get_recipe_detail_by_id(
        recipe_id,
        ["TranslatedRecipeName","TranslatedIngredients", "Cuisine", "Course", "Diet", "URL","recipe_embedding_fasttext"]
    )


    recommednded_recipies = {}

    # provide recommendations where it is required at the product page
    if with_recommendations:
        recommednded_recipies = await list_Similar_dishes(
            recipe_id,
            cuisine=cuisine,
            diet=diet,
            embeddings=recipe_details["recipe_embedding_fasttext"]
        )

    del recipe_details["recipe_embedding_fasttext"]
    print(
        {
            "basic_recipe": recipe_details,
            "recommednded_recipies" : recommednded_recipies
        }
    )

    return {
        "basic_recipe": recipe_details,
        "recommednded_recipies" : recommednded_recipies
    }



# @router.get(
#     "/name",
# )
# async def get_recipe_details_by_name(
#     recipe_name: str,
#     cuisine: List[str] = Query(None),
#     diet: List[str] = Query(None),
#     with_recommendations: bool = True,
# ):

#     # base recipe informations should be independent from its recommendations
#     recipe_details = get_recipe_detail_by_name(
#         recipe_name,
#         ["TranslatedRecipeName","TranslatedIngredients", "Cuisine", "Course", "Diet", "URL","recipe_embedding_fasttext"]
#     )

#     recommednded_recipies = {}

#     # provide recommendations where it is required at the product page
#     if with_recommendations:
#         recommednded_recipies = await list_similar_dishes_by_name(
#             recipe_name,
#             cuisine=cuisine,
#             diet=diet,
#             embeddings=recipe_details["recipe_embedding_fasttext"]
#         )

#     del recipe_details["recipe_embedding_fasttext"]
#     print(
#         {
#             "basic_recipe": recipe_details,
#             "recommednded_recipies" : recommednded_recipies
#         }
#     )

#     return {
#         "basic_recipe": recipe_details,
#         "recommednded_recipies" : recommednded_recipies
#     }
