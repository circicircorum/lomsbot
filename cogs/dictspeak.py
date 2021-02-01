import discord
from discord.ext import commands
import random
import json
import io
import aiohttp

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
            print('Error while finding the upload channel.')
            raise


    @commands.group()
    @commands.is_owner()
    async def react(self, ctx):
        if self.upload_channel is None:
            return await ctx.send('Please wait for the bot to be ready (channel not found).')


    @react.command(name='upload')
    async def upload_reaction_media(self, ctx, file_type, reaction_name, link):
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
    async def add_reaction_to_dict(self, ctx, dict_name, reaction_name, link, option=None):
        # send error message if no such dictionary exists
        if dict_name not in self.dict_dict.keys():
            await ctx.send('Error: No dictionary named ' + dict_name + ' found.')
            return
        
        # add reaction if no reaction by the same name exists
        if reaction_name not in self.dict_dict[dict_name].keys():
            self.dict_dict[dict_name][reaction_name] = [link]
            await ctx.send('Added ' + reaction_name + ' to ' + dict_name + '.')
            return
        
        # handle situations where a reaction by the same name already exists
        if option == "replace":
            self.dict_dict[dict_name][reaction_name] = [link]
            await ctx.send('Replaced ' + reaction_name + ' in ' + dict_name + '.')
        elif option == "overload":
            self.dict_dict[dict_name][reaction_name].append(link)
            await ctx.send('Overloaded ' + reaction_name + ' in ' + dict_name + '.')
        else:
            await ctx.send('Error: another reaction with the same name already exists.')
        return


    @react.command(name='remove')
    async def remove_reaction_from_dict(self, ctx, dict_name, reaction_name):
        # send error message if no such dictionary exists
        if dict_name not in self.dict_dict.keys():
            await ctx.send('Error: No dictionary named ' + dict_name + ' found.')
            return
            
        # send error message if no such reaction exists
        if reaction_name not in self.dict_dict[dict_name]:
            await ctx.send('Error: No reaction named ' + reaction_name + ' found in ' + dict_name + '.')
            return
        
        self.dict_dict[dict_name].pop(reaction_name)
        await ctx.send('Removed ' + reaction_name + ' from ' + dict_name + '.')


    @react.command(name='save')
    async def save_dict_to_file(self, ctx, prefix=''):
        # save dictionaries to JSON files
        for name, dictionary in self.dict_dict.items():
            with open(self.dir_prefix + name + '.json', 'w', encoding='utf-8') as f:
                json.dump(dictionary, f, indent=4)
                
        await ctx.send('Saved dictionaries to file.')


    @commands.Cog.listener()
    async def on_message(self, message):

        # check if the prefix matches
        if len(message.content) == 0 or message.content[0] not in self.command_prefix:
            return
        
        # extract command name
        msg_tokens = message.content.split()
        cname = msg_tokens[0][1:]

        # search dictionaries for command
        for dictionary in self.dict_dict.values():

            # check if the command is in the dictionary
            if cname in dictionary.keys():
                
                # randomly select a message if the command is overloaded
                if len(dictionary[cname]) > 1:
                    await message.channel.send(random.choice(dictionary[cname]))
                else:
                    await message.channel.send(dictionary[cname][0])
    

    @commands.command(name='list')
    async def list_dict(self, ctx, dict_name=None, sort=None):
        # list dictionaries if no dict_name is given
        if dict_name is None:
            await ctx.send('List of dictionaries: \n```\n'
                            + '\n'.join([name for name in self.dict_dict.keys()])
                            + '```')
            return

        # send error message if no such dictionary exists
        if dict_name not in self.dict_dict.keys():
            await ctx.send('Error: No dictionary named ' + dict_name + ' found.')
            return
        
        # send the list of commands in the dictionary
        entries = [cname for cname in self.dict_dict[dict_name]]

        # sort entries if required
        if sort == 'sort':
            entries.sort()
        
        entries = '\n'.join(entries)
        await ctx.send('List of entries in dictionary: \n```\n'
                        + entries
                            + '```')
    

    def init_dict(self, filenames, names):
        # initialise an empty dictionary of dictionaries
        self.dict_dict = {}

        # load dictionaries
        for i, filename in enumerate(filenames):
            with open(self.dir_prefix + filename, 'r', encoding='utf-8') as f:
                dictionary = json.load(f)
            
            # turn all strings into lists
            for reaction in dictionary:
                if isinstance(dictionary[reaction], str):
                    dictionary[reaction] = [dictionary[reaction]]

            # store the dictionary with its name
            self.dict_dict[names[i]] = dictionary
