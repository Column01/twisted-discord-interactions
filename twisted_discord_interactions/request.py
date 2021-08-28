import json


class RequestData:
    def __init__(self, request):
        content = request.content.read().decode("utf-8")
        try:
            json_data = json.loads(content)
            for k, v in json_data.items():
                setattr(self, k, v)
        except json.JSONDecodeError as e:
            print("Error decoding JSON data! {}".format(e))
    
    def get_name(self):
        return self.data.get("name")
