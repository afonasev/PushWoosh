import json


def dumps(v):
    return json.dumps(v, ensure_ascii=False)
