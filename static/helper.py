import streamlit as st
import requests
import pandas as pd
from PIL import Image
from typing import List
import json
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

LOCALHOST_SEED_URL =  "http://localhost:"
PORT = "8000"
GET_ALL_DATA_ENDPOINT = "/api/v1/recipe"
GET_RECOMMENDATIONS_ENDPOINT = "/api/v1/recipe/<id>"
SAVE_FEEDBACK_ENDPOINT = "/api/v1/feedback/"
GET_FEEDBACK_ENDPOINT = "/api/v1/feedback/"
CUISINE_OPTIONS = ['Indian', 'South Indian Recipes', 'Andhra', 'Udupi', 'Mexican', 'Fusion', 'Continental', 'Bengali Recipes', 'Punjabi', 'Chettinad', 'Tamil Nadu', 'Maharashtrian Recipes', 'North Indian Recipes', 'Italian Recipes', 'Sindhi', 'Thai', 'Chinese', 'Kerala Recipes', 'Gujarati Recipes\ufeff', 'Coorg', 'Rajasthani', 'Asian', 'Middle Eastern', 'Coastal Karnataka', 'European', 'Kashmiri', 'Karnataka', 'Lucknowi', 'Hyderabadi', 'Side Dish', 'Goan Recipes', 'Arab', 'Assamese', 'Bihari', 'Malabar', 'Himachal', 'Awadhi', 'Cantonese', 'North East India Recipes', 'Sichuan', 'Mughlai', 'Japanese', 'Mangalorean', 'Vietnamese', 'British', 'North Karnataka', 'Parsi Recipes', 'Greek', 'Nepalese', 'Oriya Recipes', 'French', 'Indo Chinese', 'Konkan', 'Mediterranean', 'Sri Lankan', 'Haryana', 'Uttar Pradesh', 'Malvani', 'Indonesian', 'African', 'Shandong', 'Korean', 'American', 'Kongunadu', 'Pakistani', 'Caribbean', 'South Karnataka', 'Appetizer', 'Uttarakhand-North Kumaon', 'World Breakfast', 'Malaysian', 'Dessert', 'Hunan', 'Dinner', 'Snack', 'Jewish', 'Burmese', 'Afghan', 'Brunch', 'Jharkhand', 'Nagaland', 'Lunch']
COURSE_OPTIONS = ['Side Dish', 'Main Course', 'South Indian Breakfast', 'Lunch', 'Snack', 'High Protein Vegetarian', 'Dinner', 'Appetizer', 'Indian Breakfast', 'Dessert', 'North Indian Breakfast', 'One Pot Dish', 'World Breakfast', 'Non Vegeterian', 'Vegetarian', 'Eggetarian', 'No Onion No Garlic (Sattvic)', 'Brunch', 'Vegan', 'Sugar Free Diet']
DIET_OPTIONS = ['Diabetic Friendly', 'Vegetarian', 'High Protein Vegetarian', 'Non Vegeterian', 'High Protein Non Vegetarian', 'Eggetarian', 'Vegan', 'No Onion No Garlic (Sattvic)', 'Gluten Free', 'Sugar Free Diet']
BLANK_IMAGE_PATH = "/home/somi/ampba/fp1/app/chef/static/blank_image.jpg"
DATA_FILE_PATH = "/home/somi/ampba/fp1/chef/data/external/df_indianRecipes.pkl"



@st.cache(allow_output_mutation=True,suppress_st_warning=True)
def get_all_recipe(
    path = DATA_FILE_PATH
):
    recipe_df = pd.read_pickle(path)
    return recipe_df


@st.cache
def get_recipe_with_recommendations(
    recipe_id : int,
    cuisine: List[str],
    diet: List[str],
    url = f"{LOCALHOST_SEED_URL}{PORT}{GET_RECOMMENDATIONS_ENDPOINT}",

):
    # modify the url according to the recipe ID
    payload = {
        "cuisine": cuisine,
        "diet": diet
    }
    response = requests.get(
        url = url.replace("<id>",f"{recipe_id}"),
        params=payload
    )
    response.raise_for_status()
    response_json = response.json()

    return response_json
    

@st.cache
def get_default_image(
    image_path = BLANK_IMAGE_PATH
):  
    image = Image.open(image_path)
    return image
    

def save_feedback(
    base_recipe: str,
    feed_value: bool,
    url:str = f"{LOCALHOST_SEED_URL}{PORT}{SAVE_FEEDBACK_ENDPOINT}",
):
    data = {
        "feed": feed_value,
        "base_recipe_name": base_recipe
    }
    response = requests.post(
        url = url,
        data=data
    )
    response.raise_for_status()
    

def get_feedback(
    url:str = f"{LOCALHOST_SEED_URL}{PORT}{GET_FEEDBACK_ENDPOINT}"
):  
    response = requests.get(
        url = url
    )
    response.raise_for_status()
    return response.json()


def make_chart(df:pd.DataFrame):
    x = df.groupby(["capture_time", "feed"]).agg("size").unstack(level=-1)
    x["pos_percent"] = (x[1]/( x[0]+x[1]))*100
    x["total"] = 100 

    fix = plt.figure(figsize=(9, 7))
    # bar chart 2 -> bottom bars (group of 'smoker=Yes')
    bar2 = sns.barplot(x=x.index, y="total", data=x, color='#A60628', alpha = 0.7,linewidth = 2, edgecolor="black")
    # bar chart 1 -> top bars (group of 'smoker=No')
    bar1 = sns.barplot(x=x.index,  y="pos_percent", data=x, color='#348ABD',alpha = 0.7,linewidth = 2, edgecolor="black")

    bar1.set_title(
        "Feedback Comparision"
    )
    bar1.set_xlabel("Days")
    bar1.set_ylabel("Percentage of Feeds")
    sns.set_style("white")
    for p in bar1.patches:
        bar1.annotate(
            format(round(p.get_height(),2)),
            (p.get_x() + p.get_width() / 2, p.get_height()),
            ha="center",
            va="center",
            xytext=(0, 10),
            textcoords="offset points",
        )
    bar1.legend(
    handles = [
            Patch(color='#348ABD', alpha=0.7, label=f"Positive"),
            Patch(color="#A60628", alpha=0.7, label=f"Negative")
        ]
    )
    sns.despine()
    return fix

def borders():
    # css injection
    max_width_str = "max-width: 1900px;"
    st.markdown(
        f"""
    <style>
    .block-container {{
        {max_width_str}
        }}
    .custom-widget {{
        display: grid;
        border: 2px solid black;
        padding: 12px;
        border-radius: 5%;
        color: #003366;
        margin-bottom: 5px;
        min-height: 251.56px;
        align-items: center;
    }}
    h6 {{
        display: block;
        font-size: 18px;
        margin-left: 0;
        margin-right: 0;
        font-weight: bold;
        color: #003366;
    }}
    h2 {{
        text-decoration: underline;
    }}
    h1 {{
        display: grid;
        justify-content: center;
        align-items: center;
    }}

    .css-1m8p54g{{
        justify-content: center;
    }}
    .css-1bt9eao {{
    }}
    .row-widget.stCheckbox {{
        display: grid;
        justify-content: center;
        align-items: center;
        border: solid 2px black;
        border-radius: 3%;
        height: 50px;
        background-color: #DF1B88;
        color: #FFFFFF;
    }}
    .css-1djdyxw {{
        color: #FFFFFF;
    }}
    .css-ps6290 {{
        color: black;
    }}
    .css-1cpxqw2 {{
        background-color: #00AB55;
        color: white;
        font-weight: 500;
        border: 1px solid #003366;
    }}
    <style>
    """,
        unsafe_allow_html=True,
    )