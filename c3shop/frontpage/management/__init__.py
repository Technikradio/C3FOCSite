import os
from .messages import load_in_data


this_dir, this_filename = os.path.split(__file__)
MESSAGE_PATH = os.path.join(this_dir, "data", "messages.csv")

load_in_data(MESSAGE_PATH)
