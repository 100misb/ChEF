# basic imports
from logging import basicConfig
from turtle import onclick, right
import streamlit as st
import pandas as pd

import helper
from streamlit_elements import elements, mui, html
from streamlit_card import card

# The code below is for the layout of the page
if "widen" not in st.session_state:
    layout = "wide"
else:
    layout = "centered" if st.session_state.widen else "wide"


st.set_page_config(
    layout=layout,
    page_title="ChEF - Choose Everyday Food",
)

# helper.borders()
# Get all the recipe dataset from the ChEF-server
recipe_df = helper.get_all_recipe()


tab1, tab2 = st.tabs(["Main", "Stats"])

with tab1:

    # This section represent the sidebar options for the 
    with st.sidebar:
        
        # Side bar section will consist mostly filters to create the profile for the user
        st.write("Enlighten us!")

        # Diet preference will provided selectbox
        diet_pref = st.selectbox(
            label="I am a",
            options = helper.DIET_OPTIONS
        )
        
        # if no diet preferences were provided then assume all
        diet_pref = helper.DIET_OPTIONS if not diet_pref else [diet_pref]
        
        if diet_pref:
            # create the final dataframe on the basis of filters
            mask_recipe_df = recipe_df[
                recipe_df["Diet"].isin(diet_pref)
            ]
        
        # Cuisines will have options to select one or more 
        cuisine_pref = st.multiselect(
            label = "Would love to try",
            options = list(mask_recipe_df["Cuisine"].unique())
        )

        cuisine_pref = list(mask_recipe_df["Cuisine"].unique()) if not cuisine_pref else cuisine_pref
        
        if cuisine_pref :
            # create the final dataframe on the basis of filters
            mask_recipe_df = mask_recipe_df[
                (mask_recipe_df["Cuisine"].isin(cuisine_pref))
            ]

    # in the main page of the tab we should show all the recipies
    select_recipe = st.selectbox(
        label="Select your dish",
        options=mask_recipe_df.index.tolist(),
        format_func = lambda x: mask_recipe_df.loc[x,"TranslatedRecipeName"],
        disabled = False
    )

    if select_recipe : 
        
        # make requests to get the recipe details and recommendations
        basic_recipe_container = st.container()
        with basic_recipe_container:
                
            recommedations = helper.get_recipe_with_recommendations(
                recipe_id=select_recipe,
                cuisine=cuisine_pref,
                diet=diet_pref
            )

            detail_col, image_col = st.columns([6,4])
            with detail_col :
                st.info(
                    f'{recommedations["basic_recipe"].get("Course")}, {recommedations["basic_recipe"].get("Cuisine")}, {recommedations["basic_recipe"].get("Diet")}'
                )

                with st.expander("Ingredients"):
                    for idx, each_text in enumerate(recommedations["basic_recipe"].get("TranslatedIngredients").split(","), 1):
                        st.write(f"{idx}. {each_text}")
                pass
            
            with image_col: 
                st.image(
                    helper.get_default_image(),caption = recommedations["basic_recipe"]["TranslatedRecipeName"] 
                )

        recommended_recipe_container = st.container()
        with recommended_recipe_container:
            st.subheader("See Similar results")
            size_mapping = [3,1]
            for col_idx, recommedation in enumerate(recommedations["recommednded_recipies"],0):
                with st.container():
                    left_pane, right_pane = st.columns(size_mapping)
                    # [3,1]
                    with left_pane:
                        st.markdown(f'###### {recommedation["TranslatedRecipeName"]}')
                        st.info(
                            f'{recommedation.get("Course")}, {recommedation.get("Cuisine")}, {recommedation.get("Diet")}'
                        )
                        with st.expander("Ingredients"):
                            for idx, each_text in enumerate(recommedation.get("clean_ingredients"), 1):
                                st.write(f"{idx}. {each_text.title()}")
                    with right_pane :
                        st.image(helper.get_default_image())
            
        st.header("")
        feedback_container = st.container()
        with feedback_container:
            good, content, bad = st.columns([1,3,1])

            with good:
                good_button = st.button(
                    label = "👍",
                    # on_click= helper.save_feedback(
                    #     base_recipe=recommedations["basic_recipe"]["TranslatedRecipeName"],
                    #     feed_value=True
                    # )
                )
                if good_button :
                    helper.save_feedback(
                        base_recipe=recommedations["basic_recipe"]["TranslatedRecipeName"],
                        feed_value=True
                    )
        
            with content :
                st.warning("Are these recommendations helpful!")

            with bad :
                bad_button = st.button(
                    label = "👎",
                    # on_click= helper.save_feedback(
                    #     base_recipe=recommedations["basic_recipe"]["TranslatedRecipeName"],
                    #     feed_value=False
                    # )
                )
                if bad_button : 
                    helper.save_feedback(
                        base_recipe=recommedations["basic_recipe"]["TranslatedRecipeName"],
                        feed_value=False
                    )


with tab2:
    feedback_data = helper.get_feedback()
    df = pd.DataFrame(feedback_data)
    st.pyplot(helper.make_chart(df), clear_figure=True)
