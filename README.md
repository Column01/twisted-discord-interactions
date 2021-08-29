# twisted-discord-interactions

A Twisted-based Python discord interactions web server implementation

Heavily inspired by the existing [discord-interactions.py](https://github.com/LiBa001/discord-interactions.py) project

## Installation

WIP

## Example Usage

```python
from twisted_discord_interactions import RequestData, InteractionClient, InteractionCommand, CommandOption, CommandOptionType

def my_command_callback(request_data: RequestData):
    do_something = True
    return b"Text response to interaction"


if __name__ == "__main__":
    pub_key = open("key.txt", "r").read().strip("\n")
    client = InteractionClient(pub_key)
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
```
