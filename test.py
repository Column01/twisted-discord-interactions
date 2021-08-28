from twisted_discord_interactions.client import InteractionClient
from twisted_discord_interactions.request import RequestData
from twisted_discord_interactions.command import InteractionCommand, CommandOption, CommandOptionType

def my_command_callback(request_data: RequestData):
    print(request_data.__dict__)
    return b"Text response to interaction"


if __name__ == "__main__":
    client = InteractionClient()
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
    client.register_command(test_command, my_command_callback)
    client.start_site()
