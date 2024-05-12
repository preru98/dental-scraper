import json
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        print("Object--------", obj)
        if isinstance(obj, str):
            return obj.encode('utf-8').decode('unicode-escape')
        return json.JSONEncoder.default(self, obj)

