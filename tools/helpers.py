import json


def json_read(path): 
    allowed_tails = ['json,', 'jsonl']
    path_tail = path.split('.')[-1]
    if path_tail in allowed_tails: 
        result = json.loads(open(path, 'r',  encoding="utf-8"))
        return result