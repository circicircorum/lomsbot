import constants
import discord
from warnings import warn
from typing import Callable


class Command():
    def __init__(self, name):
        self.name = name
    

    async def action(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'discord_message':
                discord_message = value
            else:
                warn("{0} is not a valid argument for this function".format(key))
        
        try:
            await discord_message.channel.send(self.name + ': Performing default command...')
        except NameError:
            warn(EMPTY_MESSAGE_OBJ)
            print()



class SendMessageCommand(Command):
    def __init__(self, name, message_text, description=None):
        super(SendMessageCommand, self).__init__(name)
        self.message_text = message_text
        self.description = description
    

    async def action(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'discord_message':
                discord_message = value
            else:
                warn("{0} is not a valid argument for this function".format(key))
        
        try:
            await discord_message.channel.send(self.message_text)
        except NameError:
            warn(EMPTY_MESSAGE_OBJ)
            print()



class SendFormattedMessageCommand(Command):
    def __init__(self, name, message_type, **kwargs):
        super(SendFormattedMessageCommand, self).__init__(name)

        for key, value in kwargs.items():
            if key == 'dictionary':
                self.dictionary = value
            else:
                warn("{0} is not a valid argument for this function".format(key))
        
        self.message_type = message_type
        try:
            if self.message_type == constants.LIST_COMMAND and self.dictionary is None:
                warn("The dictionary of commands is empty.")
            elif self.message_type == constants.LIST_IMAGES_COMMAND and self.dictionary is None:
                warn("The dictionary of images is empty.")
        except NameError:
            if self.message_type == constants.LIST_COMMAND:
                warn("The dictionary of commands is empty.")
            elif self.message_type == constants.LIST_IMAGES_COMMAND:
                warn("The dictionary of images is empty.")
            
    
    async def action(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'discord_message':
                discord_message = value
            else:
                warn("{0} is not a valid argument for this function".format(key))
        
        try:
            if self.message_type == constants.LIST_COMMAND:
                dictionary_keys = [key for key in self.dictionary.keys()]
                dicionary_keys.sort()
                await discord_message.channel.send('• List of commands:\n```\n' 
                                        + '\n'.join(dictionary_keys)
                                        + '```'
                                        + '\nExample: \n'
                                        + '```!test```')
            elif self.message_type == constants.LIST_IMAGES_COMMAND:
                dictionary_keys = [key for key in self.dictionary.keys()]
                dicionary_keys.sort()
                await discord_message.channel.send('• List of reaction images:\n```\n' 
                                        + '\n'.join(dictionary_keys)
                                        + '```'
                                        + '\nExample: \n'
                                        + '```!fish```')
        except NameError:
            warn(EMPTY_MESSAGE_OBJ)
            print()