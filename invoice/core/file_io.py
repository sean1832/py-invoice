import json

def read_json(path):
    return json.load(open(path, 'r'))