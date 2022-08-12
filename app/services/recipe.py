from distutils.command.clean import clean
import pandas as pd
from app.core.config import Settings
from typing import List
from loguru import logger


settings = Settings()


def get_recipe_detail_by_id(
    recipe_id: int,
    attributes_to_show: List[str]
):  
    # provide base recipe information for a particular food id
    cleaned_data = pd.read_pickle(
        settings.DATA_FILE_PATH
    )
    return cleaned_data.loc[recipe_id, attributes_to_show].to_dict()



def get_recipe_detail_by_name(
    name: str,
    attributes_to_show: List[str]
):
    # provide base recipe information for a particular food name
    cleaned_data = pd.read_pickle(
        settings.DATA_FILE_PATH
    )

    try: 
        recipe = cleaned_data[cleaned_data["TranslatedRecipeName"] == name][attributes_to_show].to_dict()
    except Exception as e:
        logger.exception(f"Recipe Name not present: {name}")
        raise e
    else :
        return recipe
