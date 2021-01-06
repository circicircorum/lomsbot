import discord
from discord.ext import commands
import random
import json
import io
import aiohttp

SECRET_SERVER_ID = 620170948708007937
SECRET_CHANNEL_ID = 757398739223576646


class DictSpeak(commands.Cog):
    """
    Facilitates the managment of reaction images, gifs and so on.
    """


    def __init__(self, bot, command_prefix, dict_filenames, dict_names, dir_prefix, upload_channel_id=SECRET_CHANNEL_ID):
        self.bot = bot
        self.command_prefix = command_prefix
        self.upload_channel_id = upload_channel_id
        self.dir_prefix = dir_prefix
        
        # set up dictionaries
        self.init_dict(dict_filenames, dict_names)


    @commands.Cog.listener()
    async def on_ready(self):
        # check if the upload channel is available.
        self.upload_channel = self.bot.get_channel(self.upload_channel_id)
        
        if self.upload_channel is None:
            print("Error while finding the upload channel.")
            raise


    @commands.group()
    async def react(self, ctx):
        if self.upload_channel is None:
            return await ctx.send('Please wait for the bot to be ready (channel not found).')

        guild_roles = self.bot.get_guild(SECRET_SERVER_ID).roles
        if guild_roles is None:
            return await ctx.send('Please wait for the bot to be ready (guild not found).')

        if guild_roles[-1] not in ctx.message.author.roles:
            return await ctx.send('Please obtain the necessary permissions to add reaction images.')


    @react.command(name='upload')
    async def __upload_reaction(self, ctx, file_type, reaction_name, link):
        # download file using link provided
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                if resp.status != 200:
                    return await ctx.send('Error while downloading file.')
                data = io.BytesIO(await resp.read())

                # upload file to specified channel
                rfile = discord.File(data)
                rfile.filename = reaction_name + '.' + file_type
                message = await self.upload_channel.send(content=reaction_name, file=rfile)

        if message is None:
            return await ctx.send('Error while retrieving image message.')


    @react.command(name='add')    
    async def __add_reaction_to_dict(self, ctx, dict_name, reaction_name, link, force=False):
        # send error message if no such dictionary exists
        if dict_name not in self.dict_dict.keys():
            await ctx.send('Error: No dictionary named ' + dict_name + ' found.')
            return
        
        # send error message if a reaction by the same name already exists
        if reaction_name in self.dict_dict[dict_name].keys() and not force:
            await ctx.send('Error: another reaction with the same name already exists.')
            return
        
        self.dict_dict[dict_name][reaction_name] = link
        await ctx.send('Added ' + reaction_name + ' to ' + dict_name + '.')

    
    @react.command(name='remove')
    async def __remove_reaction_from_dict(self, ctx, dict_name, reaction_name):
        # send error message if no such dictionary exists
        if dict_name not in self.dict_dict.keys():
            await ctx.send('Error: No dictionary named ' + dict_name + ' found.')
            return
        
        self.dict_dict[dict_name].pop(reaction_name)
        await ctx.send('Removed ' + reaction_name + ' from ' + dict_name + '.')


    @react.command(name='save')
    async def __save_and_sync_(self, ctx, prefix=''):
        # save dictionaries to JSON files
        for name, dictionary in self.dict_dict.items():
            with open(self.dir_prefix + name + '.json', 'w', encoding='utf-8') as f:
                json.dump(dictionary, f, indent=4)
                
        await ctx.send('Saved dictionaries to file.')


    @commands.Cog.listener()
    async def on_message(self, message):

        # check if the prefix matches
        if len(message.content) == 0:
            return

        if message.content[0] in self.command_prefix:
            
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
    

    @commands.command(name='list')
    async def list_dict(self, ctx, dict_name=None, sort=None):
        # check if a dict_name was given
        if dict_name is None:
            await ctx.send('List of dictionaries: \n```\n'
                            + '\n'.join([name for name in self.dict_dict.keys()])
                            + '```')
        
        # send the list of commands in the dictionary
        elif dict_name in self.dict_dict.keys():
            entries = [cname for cname in self.dict_dict[dict_name]]

            # sort entries if required
            if sort == "sort":
                entries.sort()
            
            entries = '\n'.join(entries)
            await ctx.send('List of entries in dictionary: \n```\n'
                            + entries
                            + '```')
        
        # send error message if no such dictionary exists
        else:
            await ctx.send('Error: No dictionary named ' + dict_name + ' found.')
    

    def init_dict(self, filenames, names):
        # initialise an empty dictionary of dictionaries
        self.dict_dict = {}

        # load dictionaries
        for i, filename in enumerate(filenames):
            with open(self.dir_prefix + filename, 'r', encoding='utf-8') as f:
                dictionary = json.load(f)

            # store the dictionary with its name
            self.dict_dict[names[i]] = dictionary
