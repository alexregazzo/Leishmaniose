import json



def get_data() -> dict:
    with open("dados.json", encoding="utf8") as f:
        return json.load(f)

