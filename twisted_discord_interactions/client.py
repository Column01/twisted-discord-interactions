from twisted.internet import reactor
from twisted.web import server
from twisted.web.resource import Resource
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from .interactions import Interaction, PingInteraction
from .request import RequestData


def test_command_callback(_):
    return b"TEST COMMAND PROCESSED!"


class InteractionClient(Resource):
    isLeaf = True
    
    def __init__(self, public_key):
        self.pages = {}
        self.commands = {}
        self.ping_message = PingInteraction()
        self.site = server.Site(self)
        self.verify_key = VerifyKey(bytes.fromhex(public_key))
        
    def start_site(self):
        reactor.listenTCP(8080, self.site)
        reactor.run()

    def render_GET(self, _):
        """ Generic get request so it doesn't break everything """
        return b"Root Page"
    
    def render_POST(self, request):
        """ Handles post requests to the server """
        
        # Validate the request
        signature = request.requestHeaders.getRawHeaders("X-Signature-Ed25519")[0]
        timestamp = request.requestHeaders.getRawHeaders("X-Signature-Timestamp")[0]
        try:
            msg_obj = "{}{}".format(timestamp, request.content.read().decode("utf-8"))
            self.verify_key.verify(msg_obj.encode(), bytes.fromhex(signature))
        except BadSignatureError:
            request.setResponseCode(401)
            return b"invalid request signature"

        # Parse the request data into an easy to use object
        request_data = RequestData(request)
        # It's a ping post request, reply to it.
        if request_data.type == 1:
            return self.ping_message.trigger(request)
        else:
            name = request_data.get_name()
            cmd = self.commands.get(name)
            interaction = Interaction(cmd[2], cmd[1])
            return interaction.trigger(request_data)
    
    def register_command(self, command, callback):
        self.commands[command.name] = (command.name, callback, command)
