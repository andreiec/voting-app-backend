import json
from bson import ObjectId
from rest_framework import serializers


 # JSON Encoder for ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, item):
        if isinstance(item, ObjectId):
            return str(item)
        return json.JSONEncoder.default(self, item)


# ObjectId JSON Field
class JSONField(serializers.Field):
    def to_representation(self, value):
        try:
            result = json.dumps(value, skipkeys=True, allow_nan=True,cls=JSONEncoder)
            return result
        except ValueError:
            return ''