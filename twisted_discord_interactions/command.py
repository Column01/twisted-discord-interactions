import inspect
from dataclasses import dataclass
from enum import Enum
from typing import List, Union


class CommandOptionType(Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8


@dataclass()
class CommandChoice:
    name: str
    value: Union[str, int]

    def get_choice(self):
        return {k: v for k, v in inspect.getmembers(self)}


@dataclass()
class CommandOption:
    type: CommandOptionType
    name: str
    description: str
    required: bool = False
    choices: List[CommandChoice] = None
    options: List["CommandOption"] = None

    def get_option(self):
        temp = {
            "type": self.type.value,
            "name": self.name,
            "description": self.description,
            "default": self.default,
            "required": self.required,
        }
        if self.choices:
            temp["choices"] = [choice.get_choice() for choice in self.choices]
        if self.options:
            temp["options"] = [option.get_option() for option in self.options]
        return temp


class InteractionCommand:
    def __init__(self,
        name: str,
        description: str,
        id: int,
        application_id: int,
        options: List[CommandOption] = None,
        default_permissions: bool = True,
    ):
        self.id = id
        self.application_id = application_id
        self.name = name
        self.description = description
        self.options = options or None
        self.default_permissions = default_permissions
    
    def add_option(self, option: CommandOption):
        self.options = [option] if self.options is None else self.options.append(option)

    def get_command(self):
        temp = {k: v for k, v in inspect.getmembers(self) if k != "options"}
        if self.options:
            temp["options"] = [option.get_option() for option in self.options]    
        return temp
