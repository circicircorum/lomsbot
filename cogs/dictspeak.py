import discord
from discord.ext import commands
import random
import json


class DictSpeak(commands.Cog):
    '''
    class DictSpeak(commands.Cog)

    For simple message look-ups.
    '''


    def __init__(self, bot, command_prefix, dict_filenames, dict_names):
        self.bot = bot
        self.command_prefix = command_prefix
        
        # set up dictionaries
        self.init_dict(dict_filenames, dict_names)


    @commands.Cog.listener()
    async def on_message(self, message):

        # check if the prefix matches
        if len(message.content) == 0:
            return

        if message.content[0] == self.command_prefix:
            
            # extract comamnd name
            msg_tokens = message.content.split()
            cname = msg_tokens[0][1:]

            # search dictionaries for command
            for dictionary in self.dict_dict.values():

                # check if the command is in the dictionary
                if cname in dictionary.keys():
                    
                    # send the message directly if the entry is a string
                    if isinstance(dictionary[cname], str):
                        await message.channel.send(dictionary[cname])
                    
                    # choose one of the possible options if the entry is a list
                    elif isinstance(dictionary[cname], list):
                        await message.channel.send(random.choice(dictionary[cname]))
    

    @commands.command()
    async def list(self, ctx, dict_name=None):
        # check if a dict_name was given
        if dict_name is None:
            await ctx.send('List of command dictionaries: \n```\n'
                            + '\n'.join([name for name in self.dict_dict.keys()])
                            + '```')
        
        # send the list of commands in the dictionary
        elif dict_name in self.dict_dict.keys():
            await ctx.send('List of commands in dictionary: \n```\n'
                            + '\n'.join([cname for cname in self.dict_dict[dict_name]])
                            + '```')
        
        # send error message if no such dictionary exists
        else:
            await ctx.send('Error: No dictionary named ' + dict_name + ' found.')


    def init_dict(self, filenames, names):
        # initialise an empty dictionary of dictionaries
        self.dict_dict = {}

        # load dictionaries
        for i, filename in enumerate(filenames):

            with open(filename, 'r', encoding='utf-8') as f:
                dictionary = json.load(f)

            # store the dictionary with its name
            self.dict_dict[names[i]] = dictionary
