import pandas as pd

path = "/home/somi/ampba/fp1/chef/data/external/df_indianRecipes.pkl"

df = pd.read_pickle(path)
# print(df.head())
print(list(df["Course"].unique()))
print(list(df["Diet"].unique()))


# create the final dataframe on the basis of filters
mask_recipe_df = df[
    (df["Diet"].isin(["High Protein Non Vegetarian"]))&
    (df["Cuisine"].isin(["Indian"]))
]

print(mask_recipe_df.index)
print(df.loc[280:340,"TranslatedRecipeName"])