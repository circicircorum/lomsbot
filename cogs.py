import discord
from discord.ext import commands
import random
import json
import re

class DictSpeak(commands.Cog):
    '''
    DictSpeak(bot, command_prefix)

    For simple message look-ups.
    '''
    def __init__(self, bot, command_prefix, dict_filenames, dict_names):
        self.bot = bot
        self.command_prefix = command_prefix
        
        # set up dictionaries
        self.init_dict(dict_filenames, dict_names)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content[0] == self.command_prefix:
            msg_tokens = message.content.split()
            cname = msg_tokens[0][1:]
            for _, dictionary in self.dict_dict:
                if cname in dictionary.keys():
                    if isinstance(dictionary[cname], str):
                        await message.channel.send(dictionary[cname])
                    elif isinstance(dictionary[cname], list):
                        await message.channel.send(random.choice(dictionary[cname]))
    
    @commands.command()
    async def list(self, ctx, dict_name=None):
        if dict_name is None:
            await ctx.send('List of command dictionaries: \n```\n' + '\n'.join([name for name in self.dict_dict.keys()]) + '```')
        elif dict_name in self.dict_dict.keys():
            await ctx.send('List of commands in dictionary: \n```\n' + '\n'.join([cname for cname in self.dict_dict[dict_name]]) + '```')
        else:
            await ctx.send('Error: No dictionary named ' + dict_name + ' found.')


    def init_dict(self, filenames, names):
        self.dict_dict = {}

        # load dictionaries
        for i, filename in enumerate(filenames):
            with open(filename, 'r', encoding='utf-8') as f:
                dictionary = json.load(f)
            self.dict_dict[names[i]] = dictionary
