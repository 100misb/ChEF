from turtle import settiltangle
from fastapi import APIRouter, Form
from datetime import date, datetime
from app.core.config import Settings
import json
from app.services.feedback import check_or_create_feedback_file

settings = Settings()
router = APIRouter()

@router.post(
    "/"
)
async def capture_feedback(
    feed: bool = Form(...), 
    base_recipe_name:str = Form(...)
):
    # now = datetime.now()
    now = date.today()
    feed_query = {}

    feed_query["capture_time"] = now
    feed_query["base_recipe"] = base_recipe_name
    feed_query["feed"] = int(feed)

    check_or_create_feedback_file(settings.FEEDBACK_FILE)

    with open(str(settings.FEEDBACK_FILE),'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(feed_query)
        # Sets file's current position at offset.
        file.seek(0)

        # convert back to json.
        json.dump(file_data, file, indent = 2, default=str)
    
    return feed_query


@router.get(
    "/"
)
async def retrieve_feedback():
    feedback_file = settings.FEEDBACK_FILE
    if not feedback_file.exists():
        return {}
    
    with open(str(settings.FEEDBACK_FILE),'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
    
    return file_data