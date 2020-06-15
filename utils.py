import json
import os


def get_data() -> dict:
    with open(os.path.join(CURRENT_DIRPATH, "dados.json"), encoding="utf8") as f:
        return json.load(f)

CURRENT_DIRPATH = os.path.dirname(__file__)
