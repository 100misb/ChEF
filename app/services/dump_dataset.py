from typing import Final
import pandas as pd
import sqlite3

SOURCE_CLEANED_DATASET = "/home/somi/ampba/fp1/chef/data/external/df_indianRecipes.pkl"
DB_PATH = "food_recipe.db"

# read dataset from source: 
df_pkl = pd.read_pickle(SOURCE_CLEANED_DATASET)
df_pkl.drop(columns=["URL"], inplace = True)
# df_pkl["TranslatedInstructions"] =df_pkl["TranslatedInstructions"].fillna("")

print(df_pkl.columns)
print(df_pkl.iloc[0])
try:
    # create_table_query = """CREATE TABLE IF NOT EXISTS ARCHANA_KITCHEN (TranslatedRecipeName TEXT, TranslatedIngredients TEXT, Cuisine TEXT, Course TEXT, Diet TEXT, TranslatedInstructions TEXT, clean_ingredient TEXT, ingredient_count INTEGER, clean_instructions TEXT, recipe_embedding_fasttext TEXT)"""
    conn = sqlite3.connect(DB_PATH)
    df_pkl.to_sql("ARCHANA_KITCHEN", conn, if_exists='replace', index = False)
    conn.commit()
    # c = conn.cursor()
except sqlite3.Error as e:
    print("Error while connecting to sqlite", e)
finally:
    if conn:
        conn.close()
        print("The SQLite connection is closed")
