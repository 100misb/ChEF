import json
from pathlib import Path
# from app.core.config import Settings

from pathlib import Path
file_path = Path(__file__).resolve()
data_folder = file_path.parents[1] / "data"


def check_or_create_feedback_file(feedback_file):

    if not isinstance(feedback_file, str):
        feedback_file = Path(feedback_file)
    
    if not feedback_file.exists():
        with open(str(feedback_file), "w+") as f:
            f.write(json.dumps([]))
    return True