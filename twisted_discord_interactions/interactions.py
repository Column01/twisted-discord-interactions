import json
from command import InteractionCommand


class Interaction:
    payload = ""
    """ An interaction endpoint """
    def __init__(
        self,
        command: InteractionCommand = None,
        callback = None
    ):
        if command:
            self.command = command
        if callback:
            self.callback = callback
        else:
            self.callback = self.handle

    def handle(self, _):
        return self.get_payload().encode("utf-8")

    def get_payload(self):
        if isinstance(self.payload, dict):
            return json.dumps(self.payload)
        else:
            return self.payload

    def trigger(self, request_data):
        return self.callback(request_data)


class PingInteraction(Interaction):
    payload = {"type": 1}
