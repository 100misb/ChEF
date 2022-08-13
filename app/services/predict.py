from distutils.command.clean import clean
import os
import pandas as pd
from typing import List

from app.core.errors import PredictException, ModelLoadException
from app.core.config import MODEL_NAME, MODEL_PATH, Settings
from loguru import logger

from numpy import dot
from numpy.linalg import norm
import numpy as np

# SOURCE_CLEANED_DATASET = "/home/somi/ampba/fp1/chef/data/external/df_indianRecipes.pkl"
settings = Settings()


class MachineLearningModelHandlerScore(object):
    model = None

    @classmethod
    def predict(cls, input, load_wrapper=None, method="predict"):
        clf = cls.get_model(load_wrapper)
        if hasattr(clf, method):
            return getattr(clf, method)(input)
        raise PredictException(f"'{method}' attribute is missing")

    @classmethod
    def get_model(cls, load_wrapper):
        if cls.model is None and load_wrapper:
            cls.model = cls.load(load_wrapper)
        return cls.model

    @staticmethod
    def load(load_wrapper):
        model = None
        if MODEL_PATH.endswith("/"):
            path = f"{MODEL_PATH}{MODEL_NAME}"
        else:
            path = f"{MODEL_PATH}/{MODEL_NAME}"
        if not os.path.exists(path):
            message = f"Machine learning model at {path} not exists!"
            logger.error(message)
            raise FileNotFoundError(message)
        model = load_wrapper(path)
        if not model:
            message = f"Model {model} could not load!"
            logger.error(message)
            raise ModelLoadException(message)
        return model

def find_Similar_dish(xx, cleaned_data: pd.DataFrame, embeddings ,embeddingToUse="recipe_embedding_fasttext"):

    if isinstance(xx, str):
        # get the index number for the recipe
        xx = cleaned_data[cleaned_data["TranslatedRecipeName"]==xx].index.values[0]

    a = embeddings
    if not embeddings.size:
        a = cleaned_data.loc[xx, embeddingToUse]

    orn = cleaned_data.loc[xx, "TranslatedRecipeName"]
    print(orn,"\nGetting most similar dishes based on",embeddingToUse)
    dishtances = {}
    for i in cleaned_data.index:
        if i==xx:
            continue
        try:
            dn = cleaned_data.loc[i, "TranslatedRecipeName"]
            b = cleaned_data.loc[i, embeddingToUse]
            cos_sim = dot(a, b)/(norm(a)*norm(b))
            if cos_sim not in dishtances.values():
                dishtances[i] = cos_sim
        except:
            continue
    
    dishtances_2 = {k: v for k, v in sorted(dishtances.items(), key=lambda item: item[1], reverse = True)}
    mostSimilarDishes = []
    countSim = 0
    for el in dishtances_2.keys():
        mostSimilarDishes.append(el)
        countSim+=1
        if countSim==10:
            break
    return mostSimilarDishes


async def list_Similar_dishes(xx, cuisine, diet, embeddings ,cleaned_data_path: str = settings.DATA_FILE_PATH, embeddingToUse = "recipe_embedding_fasttext"):

    additionalColumns = ['TranslatedRecipeName', 'Cuisine', 'Course', 'Diet', 'clean_ingredients']
    
    cleaned_data = pd.read_pickle(cleaned_data_path)
    if not cuisine :
        cuisine = list(cleaned_data["Cuisine"].unique())
    
    if not diet:
        diet = list(cleaned_data["Diet"].unique())
    
    mask_recipe_df = cleaned_data[
        (cleaned_data["Diet"].isin(diet))&
        (cleaned_data["Cuisine"].isin(cuisine))
    ]


    similarList1 = find_Similar_dish(xx=xx,cleaned_data = mask_recipe_df,embeddingToUse=embeddingToUse, embeddings=embeddings)
    
    similar_dishes = cleaned_data.loc[similarList1,additionalColumns].to_dict(orient="records")
    return similar_dishes


async def list_similar_dishes_by_name(name, cuisine, diet, embeddings ,cleaned_data_path: str = settings.DATA_FILE_PATH, embeddingToUse = "recipe_embedding_fasttext"):

    # columns to show
    additionalColumns = ['TranslatedRecipeName', 'Cuisine', 'Course', 'Diet', 'clean_ingredients']
    
    # read the cleaned dataset and filter it accordingly
    cleaned_data = pd.read_pickle(cleaned_data_path)
    if not cuisine :
        cuisine = list(cleaned_data["Cuisine"].unique())
    
    if not diet:
        diet = list(cleaned_data["Diet"].unique())
    
    mask_recipe_df = cleaned_data[
        (cleaned_data["Diet"].isin(diet))&
        (cleaned_data["Cuisine"].isin(cuisine))
    ]

    similarList1 = find_Similar_dish(xx=name,cleaned_data = mask_recipe_df,embeddingToUse=embeddingToUse, embeddings=embeddings)
    
    similar_dishes = cleaned_data.loc[similarList1,additionalColumns].to_dict(orient="records")
    return similar_dishes