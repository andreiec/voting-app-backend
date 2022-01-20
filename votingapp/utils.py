from pymongo import MongoClient
from bson import json_util

import json


# Parse from BSON to JSON
def parse_json(data):
    return json.loads(json_util.dumps(data))


# Database connection setup
def get_db(db_name, host="127.0.0.1", port=27017, username="", password=""):
    client = MongoClient(
        host=host,
        port=int(port),
        username=username,
        password=password
    )

    db_handle = client[db_name]
    return db_handle, client