from request import RequestData

from twisted.web import server
from twisted.web.resource import Resource
from twisted.internet import reactor
from interactions import Interaction, PingInteraction
from command import InteractionCommand, CommandOption, CommandOptionType


def test_command_callback(_):
    return b"TEST COMMAND PROCESSED!"


class InteractionClient(Resource):
    isLeaf = True
    
    def __init__(self):
        self.pages = {}
        self.commands = {}
        self.ping_message = PingInteraction()
        self.site = server.Site(self)
        test_command = InteractionCommand(
            name="test", 
            description="test command",
            id=0,
            application_id=0,
            options=[
                CommandOption(
                    type=CommandOptionType.STRING, 
                    name="test_val", 
                    description="Testing Value",
                    required=False
                )
            ]
        )
        self.register_command(test_command, test_command_callback)
        
    def start_site(self):
        reactor.listenTCP(8080, self.site)
        reactor.run()

    def render_GET(self, _):
        """ Generic get request so it doesn't break everything """
        return b"Root Page"
    
    def render_POST(self, request):
        """ Handles post requests to the server """
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


if __name__ == "__main__":
    resource = InteractionClient()
    resource.start_site()
